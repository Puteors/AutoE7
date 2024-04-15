import cv2
import pyautogui
import numpy as np
import os
import time
import win32gui
import threading
from tkinter import messagebox

IMAGE_PATH = "../images/"
TIME_SLEEP = 0.2
VALUE = {"buy_mys": 280_000, "buy_bm": 184_000}


class AutoRefreshShop(threading.Thread):
    def __init__(self, root, cost, ss, window_title, callback):
        threading.Thread.__init__(self)
        self.root = root
        self.running = True
        self.dt = {}
        self.total = 0
        self.total_ss = 0
        self.num_bm = 0
        self.num_mys = 0
        self.cost = cost
        self.ss = ss
        self.callback = callback
        hwnd = win32gui.FindWindow(None, window_title)
        win32gui.MoveWindow(hwnd, 0, 0, 1184, 681, True)

    def read_image(self):
        imgs = os.listdir(IMAGE_PATH)
        for img in imgs:
            self.dt[img[:-4]] = cv2.imread(IMAGE_PATH + img, cv2.IMREAD_GRAYSCALE)

    def click(self, btn_name):

        screenshot = pyautogui.screenshot()
        screen_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, self.dt[btn_name], cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        threshold = 0.8
        if max_val >= threshold:
            if btn_name in VALUE:
                self.total += VALUE[btn_name]
            if btn_name == "buy_bm":
                self.num_bm += 1
            elif btn_name == "buy_mys":
                self.num_mys += 1
            elif btn_name == "confirm":
                self.total_ss += 3
        else:
            return
        top_left = max_loc
        w, h = self.dt[btn_name].shape[::-1]
        center_x = top_left[0] + w - 50
        center_y = top_left[1] + h - 50
        pyautogui.mouseDown(x=center_x, y=center_y)
        pyautogui.mouseUp(x=center_x, y=center_y)

    def run(self):
        self.read_image()
        w, h = pyautogui.size()
        while self.running:
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

            if self.cost - self.total < 280_000 or self.ss - self.total_ss < 3:
                self.callback(self.num_bm, self.num_mys)
                return

            self.click("refresh")
            time.sleep(TIME_SLEEP)
            self.click("confirm")
            time.sleep(1)

    def get_current_state(self):
        return self.num_bm, self.num_mys
