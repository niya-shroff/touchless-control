import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

# ---------------- CONFIG ----------------
SMOOTHING = 5                 # Higher = smoother but slower cursor
FRAME_MARGIN = 100           # Ignore edges to reduce jitter
CLICK_DELAY = 0.5
RIGHT_CLICK_DELAY = 0.7

# ---------------- STATE ----------------
prev_x, prev_y = 0, 0        # Previous cursor position (for smoothing)
curr_x, curr_y = 0, 0
dragging = False             # Track drag state
last_click_time = 0          # Prevent rapid accidental clicks

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)
drawer = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()
TIP_IDS = [4, 8, 12, 16, 20]

def get_finger_states(hand_landmarks):
    """
    Returns a list like [thumb, index, middle, ring, pinky]
    where 1 = up, 0 = down
    """
    fingers = []

    # Thumb (compare x because thumb moves sideways)
    if hand_landmarks.landmark[TIP_IDS[0]].x > hand_landmarks.landmark[TIP_IDS[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers (compare y because they move vertically)
    for i in range(1, 5):
        tip = hand_landmarks.landmark[TIP_IDS[i]]
        joint = hand_landmarks.landmark[TIP_IDS[i] - 2]

        fingers.append(1 if tip.y < joint.y else 0)

    return fingers


def map_to_screen(x, y, frame_w, frame_h):
    """
    Convert camera coordinates → screen coordinates
    while ignoring outer margins
    """
    screen_x = np.interp(x,
                         (FRAME_MARGIN, frame_w - FRAME_MARGIN),
                         (0, screen_w))

    screen_y = np.interp(y,
                         (FRAME_MARGIN, frame_h - FRAME_MARGIN),
                         (0, screen_h))

    return screen_x, screen_y


def smooth_movement(target_x, target_y):
    """
    Apply simple linear smoothing to reduce jitter
    """
    global prev_x, prev_y

    curr_x = prev_x + (target_x - prev_x) / SMOOTHING
    curr_y = prev_y + (target_y - prev_y) / SMOOTHING

    prev_x, prev_y = curr_x, curr_y
    return curr_x, curr_y


def pinch_distance(lm):
    """
    Distance between thumb tip and index tip
    Used for click detection
    """
    return math.hypot(
        lm[8].x - lm[4].x,
        lm[8].y - lm[4].y
    )

while True:
    success, frame = cap.read()
    if not success:
        break

    # Mirror image for natural interaction
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Visual boundary box (active region)
    cv2.rectangle(frame,
                  (FRAME_MARGIN, FRAME_MARGIN),
                  (w - FRAME_MARGIN, h - FRAME_MARGIN),
                  (255, 0, 255), 2)

    # Convert to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            drawer.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            lm = hand.landmark
            fingers = get_finger_states(hand)

            # Index finger tip position
            ix = int(lm[8].x * w)
            iy = int(lm[8].y * h)

            # Map + smooth movement
            target_x, target_y = map_to_screen(ix, iy, w, h)
            smooth_x, smooth_y = smooth_movement(target_x, target_y)

            # Pause (all fingers up)
            if fingers == [1, 1, 1, 1, 1]:
                cv2.putText(frame, "PAUSE", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Move cursor (index only)
            elif fingers == [0, 1, 0, 0, 0]:
                pyautogui.moveTo(smooth_x, smooth_y)

            # Scroll (index + middle)
            elif fingers == [0, 1, 1, 0, 0]:
                direction = 30 if iy < h // 2 else -30
                pyautogui.scroll(direction)

            # Left click (pinch gesture)
            if pinch_distance(lm) < 0.03:
                if time.time() - last_click_time > CLICK_DELAY:
                    pyautogui.click()
                    last_click_time = time.time()

                    cv2.putText(frame, "CLICK", (20, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

            # Right click (thumb + middle)
            if fingers == [1, 0, 1, 0, 0]:
                if time.time() - last_click_time > RIGHT_CLICK_DELAY:
                    pyautogui.rightClick()
                    last_click_time = time.time()

            # Drag (closed fist)
            if fingers == [0, 0, 0, 0, 0]:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()