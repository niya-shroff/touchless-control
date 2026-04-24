import pyautogui
import time
from config import config

class MouseController:
    def __init__(self):
        self.last_click = 0
        self.dragging = False

    def move(self, x, y):
        pyautogui.moveTo(x, y)

    def click(self):
        if not config.ENABLE_CLICK:
            return
        if time.time() - self.last_click > config.CLICK_DELAY:
            pyautogui.click()
            self.last_click = time.time()

    def right_click(self):
        if not config.ENABLE_RIGHT_CLICK:
            return
        if time.time() - self.last_click > config.RIGHT_CLICK_DELAY:
            pyautogui.rightClick()
            self.last_click = time.time()

    def drag(self, is_fist):
        if not config.ENABLE_DRAG:
            return

        if is_fist and not self.dragging:
            pyautogui.mouseDown()
            self.dragging = True

        elif not is_fist and self.dragging:
            pyautogui.mouseUp()
            self.dragging = False

    def scroll(self, amount):
        if config.ENABLE_SCROLL:
            pyautogui.scroll(amount)