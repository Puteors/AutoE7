import cv2
import pyautogui
import numpy as np
import os
import time
import win32gui
import threading
import constants


class AutoRefreshShop(threading.Thread):
    def __init__(self, root, cost, ss, window_title, callback):
        threading.Thread.__init__(self)
        self.root = root
        self.isRunning = True
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
        imgs = os.listdir(constants.IMAGE_PATH)
        for img in imgs:
            self.dt[img[:-4]] = cv2.imread(
                constants.IMAGE_PATH + img, cv2.IMREAD_GRAYSCALE
            )

    def click(self, btn_name):

        screenshot = pyautogui.screenshot()
        screen_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screen_gray, self.dt[btn_name], cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        threshold = 0.8
        if max_val >= threshold:
            self.handle_button(btn_name)
        else:
            return

        self.perform_click(btn_name, max_loc)

    def handle_button(self, btn_name):

        if btn_name in constants.BUTTON_VALUES:
            self.total += constants.BUTTON_VALUES[btn_name]
        if btn_name == "buy_bm":
            self.num_bm += 1
        elif btn_name == "buy_mys":
            self.num_mys += 1
        elif btn_name == "confirm":
            self.total_ss += 3

    def perform_click(self, btn_name, max_loc):
        top_left = max_loc
        w, h = self.dt[btn_name].shape[::-1]
        center_x = top_left[0] + w - 50
        center_y = top_left[1] + h - 50
        pyautogui.mouseDown(x=center_x, y=center_y)
        pyautogui.mouseUp(x=center_x, y=center_y)

    def run(self):
        self.read_image()

        while self.isRunning:
            self.perform_actions()
            if self.should_stop():
                self.callback(self.num_bm, self.num_mys)
                return

    def perform_actions(self):
        w, h = pyautogui.size()

        for action in constants.ACTIONS:
            if action[0] == "scroll":
                pyautogui.moveTo(w // 2, h // 2)
                pyautogui.scroll(-600)
            else:
                self.click(action[0])
                if action[1]:
                    time.sleep(constants.TIME_SLEEP)
                    self.click(action[1])

            time.sleep(constants.TIME_SLEEP if action[1] != "confirm" else constants.TIME_SLEEP*3)

    def should_stop(self):
        if (
            self.cost - self.total < constants.MIN_GOLD
            or self.ss - self.total_ss < constants.MIN_SS
        ):
            return True
        else:
            return False

    def get_current_state(self):
        return self.num_bm, self.num_mys
