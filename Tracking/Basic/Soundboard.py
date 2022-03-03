from threading import Thread
import cv2
import numpy as np
import keyboard
from pygame import mixer

cap = cv2.VideoCapture(0)
mixer.init()

logo = cv2.imread('images.jpg')
size = 150
logo = cv2.resize(logo, (size, size))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

def playfile(path):
    mixer.music.load(path)
    mixer.music.play()
    while mixer.music.get_busy():
        pass

def key_read():
    while True:
        try:
            if keyboard.read_key() == '1': Thread(target=playfile, args=('./sounds/ps2.wav',)).start()
            elif keyboard.read_key() == '2': Thread(target=playfile, args=('./sounds/subse.wav',)).start()
            elif keyboard.read_key() == '3': Thread(target=playfile, args=('./sounds/yugay.wav',)).start()
            elif keyboard.read_key() == '4': Thread(target=playfile, args=('./sounds/gorp.wav',)).start()
            elif keyboard.read_key() == '5': Thread(target=playfile, args=('./sounds/birdgorp.wav',)).start()
            
        except:
            pass

Thread(target=key_read).start()

while True:
    success, img = cap.read()
    roi = img[-size-10:-10, -size-10:-10]

    roi[np.where(mask)] = 0
    roi += logo

    cv2.imshow('WebCam Overlay', img)
    if cv2.waitKey(1) == ord('q'):
        break

    cv2.waitKey(1)
