import cv2 as cv
import numpy as np
import pyautogui
import time

class FishingAgent:
    def __init__(self, main_agent) -> None:
        print("\tZone & Time:\t" + main_agent.zone, main_agent.time)
        zone = main_agent.zone
        time = main_agent.time
        string = str(zone).lower() + "_" + str(time).lower()
        fishing_target_str = "fishing_module/assets/fishing_target_" + string + ".png"

        self.main_agent = main_agent
        self.fishing_target = cv.imread(fishing_target_str)
        self.fishing_thread = None

    def cast_lure(self):
        time.sleep(2)
        print("Casting lure..")
        pyautogui.press("1")
        time.sleep(2)
        self.find_lure()

    def find_lure(self):
        if self.main_agent.curr_img is not None:
            lure_location = cv.matchTemplate(self.main_agent.curr_img, self.fishing_target, cv.TM_CCOEFF_NORMED)
            lure_location_arr = np.array(lure_location)

            # cv.imshow("Computer Vision", lure_location_arr)
            # cv.waitKey(0)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lure_location_arr)
            self.move_mouse_to_lure(max_loc)

    def move_mouse_to_lure(self, max_loc):
        pyautogui.moveTo(max_loc[0] + 30, max_loc[1], 0.5, pyautogui.easeOutQuad)
        self.watch_lure(max_loc)

    def watch_lure(self, max_loc):
        watch_time = time.time()
        
        while True:
            px = self.main_agent.curr_imgHSV[max_loc[1], max_loc[0]]
            #Only for adding new zones
            print(px[0])

            if self.main_agent.zone == "Uldum" and (self.main_agent.time == "Day" or self.main_agent.time == "Night"):
                if px[0] <= 88:
                    print("Bite")
                    break

            if self.main_agent.zone == "Deepholm" and (self.main_agent.time == "Day" or self.main_agent.time == "Night"):
                if px[0] <= 20:
                    print("Bite")
                    break

            if time.time() - watch_time >= 15:
                print("Fishing timeout")
                break

        self.pull_line()

    def pull_line(self):
        time.sleep(0.005)
        pyautogui.click(button="right")
        time.sleep(0.010)
        print("Line pulled")

    def run(self):
        while True:
            self.cast_lure()
