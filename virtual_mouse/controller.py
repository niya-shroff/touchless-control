import pyautogui
import time

class Controller:
    def __init__(self):
        self.last_click = 0
        self.dragging = False

    def move(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self):
        if time.time() - self.last_click > 0.5:
            pyautogui.click()
            self.last_click = time.time()

    def drag(self, is_fist):
        if is_fist and not self.dragging:
            pyautogui.mouseDown()
            self.dragging = True
        elif not is_fist and self.dragging:
            pyautogui.mouseUp()
            self.dragging = False

    def scroll(self, amount):
        pyautogui.scroll(amount)