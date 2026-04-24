import cv2
import mediapipe as mp

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7
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