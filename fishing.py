import time
import pyautogui
import cv2 as cv
import numpy as np
from threading import Thread
import os
from PIL import Image, ImageGrab
from Xlib import display, X
from fishing_module.fishing_agent import FishingAgent
import mss

list_zones = ["Deepholm", "Uldum"]
list_times = ["Day", "Night"]

class MainAgent:
    def __init__(self) -> None:
        self.agents = []
        self.fishing = None

        self.curr_img = None
        self.curr_imgHSV = None

        #defaults
        self.zone = "Uldum"
        self.time = "Day"

        print("main_agent setup complete.")


def update_screen(agent):

    t0 = time.time()
    fps_report_delay = 5
    fps_report_time = time.time()

    while True:
        curr_img = ImageGrab.grab()
        curr_img = np.array(curr_img)
        curr_img = cv.cvtColor(curr_img, cv.COLOR_RGB2BGR)
        curr_imgHSV = cv.cvtColor(curr_img, cv.COLOR_BGR2HSV)

        agent.curr_img = curr_img
        agent.curr_imgHSV = curr_imgHSV

        ex_time = time.time() - t0
        if time.time() - fps_report_time >= fps_report_delay:
            print("FPS: " + str(1 / (ex_time)))
            fps_report_time = time.time()
        t0 = time.time()
        time.sleep(0.005)

def print_menu():
    print("Command:")
    print('\tS\tStart screen capture.')
    print('\tF\tStart fishing.')
    print('\tZ\tChoose zone')
    print('\tQ\tQuit program.')

if __name__ == "__main__":
    main_agent = MainAgent()
    print_menu()

    while True:
        user_input = input()
        user_input = str.lower(user_input).strip()

        if user_input == 's':
            update_screen_thread = Thread(
                target=update_screen, 
                args=(main_agent,), 
                name="update screen thread",
                daemon=True)
            update_screen_thread.start()

        elif user_input == 'f':        
            fishing_agent = FishingAgent(main_agent)
            fishing_agent.run()
            
        elif user_input == 'z':
            print("Zone:")
            for i in range(0, len(list_zones)):
                print("\t"+str(i+1)+"\t" + list_zones[i])
            user_zone_input = list_zones[int(input())-1]

            print("Time:")
            for i in range(0, len(list_times)):
                print("\t"+str(i+1)+"\t" + list_times[i])
            user_time_input = list_times[int(input())-1]

            main_agent.time = user_time_input
            main_agent.zone = user_zone_input

            print_menu()

        elif user_input == 'q':
            print("Shutting down program.")
            cv.destroyAllWindows()
            break       
        else:
            print("Input error.")
            print_menu()

    print("Done.")
