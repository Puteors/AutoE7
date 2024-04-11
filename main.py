import cv2
import pyautogui
import numpy as np
import os
import keyboard
import time

IMAGE_PATH = "./images/"
TIME_SLEEP = 0.2


class AutoRefreshShop:
    def __init__(self) -> None:
        self.dt = {}

    def read_image(self):
        imgs = os.listdir(IMAGE_PATH)
        for img in imgs:
            self.dt[img[:-4]] = cv2.imread(IMAGE_PATH + img, cv2.IMREAD_GRAYSCALE)

    def click(self, btn_name):
        screenshot = pyautogui.screenshot()

        # Gray Scale
        screen_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

        # Find similar image
        result = cv2.matchTemplate(screen_gray, self.dt[btn_name], cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8
        if max_val >= threshold:
            print("Image exists on the screen.")
        else:
            print("Image does not exist on the screen.")
            return

        top_left = max_loc

        # Find center position
        w, h = self.dt[btn_name].shape[::-1]
        center_x = top_left[0] + w - 50
        center_y = top_left[1] + h - 50

        pyautogui.mouseDown(x=center_x, y=center_y)
        pyautogui.mouseUp(x=center_x, y=center_y)

    def detect_n_click(self):
        self.read_image()
        w, h = pyautogui.size()

        while not keyboard.is_pressed("esc"):

            self.click("mystic")
            time.sleep(TIME_SLEEP)

            self.click("buy_mys")
            time.sleep(TIME_SLEEP)

            self.click("bookmark")
            time.sleep(TIME_SLEEP)

            self.click("buy_bm")
            time.sleep(TIME_SLEEP)

            pyautogui.moveTo(w // 2, h // 2)            
            pyautogui.scroll(-600)
            time.sleep(TIME_SLEEP)

            self.click("mystic")
            time.sleep(TIME_SLEEP)

            self.click("buy_mys")
            time.sleep(TIME_SLEEP)

            self.click("bookmark")
            time.sleep(TIME_SLEEP)

            self.click("buy_bm")
            time.sleep(TIME_SLEEP)
            
            self.click("refresh")
            time.sleep(TIME_SLEEP)

            self.click("confirm")
            time.sleep(1)


# ["mystic", "buy_mys", "bookmark", "buy_bm", "refresh", "confirm"]

auto = AutoRefreshShop()
auto.detect_n_click()
