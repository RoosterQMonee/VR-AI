from pyautogui import * 
import pyautogui 
import time

while 1:
    if pyautogui.locateOnScreen('img.png', region=(150,175,350,600), grayscale=True, confidence=0.8) != None:
        print("I can see it")
        time.sleep(0.5)
    else:
        print("I am unable to see it")
        time.sleep(0.5)
