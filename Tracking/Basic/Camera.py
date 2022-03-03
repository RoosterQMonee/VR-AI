import cv2

cap = cv2.VideoCapture(1)

logo = cv2.imread('images.jpg')
size = 150
logo = cv2.resize(logo, (size, size))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
 
while True:
    success, img = cap.read()
    
    cv2.imshow('WebCam Overlay', img)
    if cv2.waitKey(1) == ord('q'):
        break

    cv2.waitKey(1)
