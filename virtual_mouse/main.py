import numpy as np
from vision import Vision
from controller import MouseController
from gestures import get_fingers, is_pinch
from config import config

vision = Vision()
mouse = MouseController()

prev_x, prev_y = 0, 0


def smooth(x, y):
    global prev_x, prev_y
    prev_x += (x - prev_x) / config.SMOOTHING
    prev_y += (y - prev_y) / config.SMOOTHING
    return prev_x, prev_y


while True:
    frame, data = vision.read_frame()
    if frame is None:
        break

    result, w, h = data

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            lm = hand.landmark
            fingers = get_fingers(lm)

            x = int(lm[8].x * w)
            y = int(lm[8].y * h)

            # map to screen
            screen_x = np.interp(x, (100, w-100), (0, 1920))
            screen_y = np.interp(y, (100, h-100), (0, 1080))

            sx, sy = smooth(screen_x, screen_y)

            # MOVE
            if fingers == [0,1,0,0,0]:
                mouse.move(sx, sy)

            # CLICK
            if is_pinch(lm):
                mouse.click()

            # RIGHT CLICK
            if fingers == [1,0,1,0,0]:
                mouse.right_click()

            # DRAG
            mouse.drag(fingers == [0,0,0,0,0])

            # SCROLL
            if fingers == [0,1,1,0,0]:
                mouse.scroll(30 if y < h//2 else -30)

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vision.release()
cv2.destroyAllWindows()