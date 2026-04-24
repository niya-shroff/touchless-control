import cv2
import mediapipe as mp

class Vision:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.drawer = mp.solutions.drawing_utils

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None, None
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        return frame, (result, w, h)

    def release(self):
        self.cap.release()

    def process_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        alert = None

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.drawer.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                alert = self.detect_gesture(hand_landmarks)

        return frame, alert

    def detect_gesture(self, landmarks):
        tips = [8, 12, 16, 20] 
        fingers_up = 0

        for tip in tips:
            if landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y:
                fingers_up += 1

        if fingers_up == 0:
            return "FIST DETECTED"
        elif fingers_up == 5:
            return "OPEN HAND"
        elif fingers_up == 2:
            return "SCROLL MODE"
        return None