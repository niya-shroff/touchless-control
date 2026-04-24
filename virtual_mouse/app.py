import tkinter as tk
import threading
import cv2
import numpy as np
from PIL import Image, ImageTk

from vision import Vision
from controller import MouseController
from gestures import get_fingers, is_pinch
from config import config


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Virtual Mouse Pro")

        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        self.vision = Vision()
        self.mouse = MouseController()

        self.running = True

        self.prev_x = 0
        self.prev_y = 0

        # start loop in background
        threading.Thread(target=self.loop, daemon=True).start()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    # smooth movement (no jitter)
    def smooth(self, x, y):
        self.prev_x += (x - self.prev_x) / config.SMOOTHING
        self.prev_y += (y - self.prev_y) / config.SMOOTHING
        return self.prev_x, self.prev_y

    def loop(self):
        while self.running:
            frame, data = self.vision.get_frame()
            if frame is None:
                continue

            result, w, h = data

            if result.multi_hand_landmarks:
                for hand in result.multi_hand_landmarks:
                    lm = hand.landmark
                    fingers = get_fingers(lm)

                    x = int(lm[8].x * w)
                    y = int(lm[8].y * h)

                    screen_x = np.interp(x, (100, w - 100), (0, 1920))
                    screen_y = np.interp(y, (100, h - 100), (0, 1080))

                    sx, sy = self.smooth(screen_x, screen_y)

                    # gestures
                    if fingers == [0, 1, 0, 0, 0]:
                        self.mouse.move(sx, sy)

                    if is_pinch(lm):
                        self.mouse.click()

                    self.mouse.drag(fingers == [0, 0, 0, 0, 0])

            # convert frame → Tkinter image
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            # update UI safely
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

    def close(self):
        self.running = False
        self.vision.release()
        self.root.destroy()

    def run(self):
        self.root.mainloop()