import cv2
from vision import Vision
from controller import Controller

class App:
    def __init__(self):
        self.vision = Vision()
        self.controller = Controller()

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame, alert = self.vision.process_frame(frame)

            if alert:
                cv2.rectangle(frame, (10, 10), (400, 80), (0, 0, 0), -1)
                cv2.putText(
                    frame,
                    alert,
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Touchless Control Mouse", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        self.vision.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = App()
    app.run()