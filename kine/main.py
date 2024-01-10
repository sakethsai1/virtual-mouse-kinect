import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import cv2
import numpy as np
import handtrackmodule as htm
import time
import pyautogui

width,height = 640,480
wscreen,hscreen = pyautogui.size()
smoothening = 4
pTime = 0
plocX , plocY= 0,0
clocX, clocY = 0,0

frameR = 100 # Frame reduction
arr = [0, 0, 0]
x1,y1 = 0,0


cap = cv2.VideoCapture(1) #Change to 1 if other cams
cap.set(3,width)
cap.set(4,height)
pTime = 0
detector = htm.FindHands()


while True:

    #find hand landmarks
    success, img = cap.read()

    #finger_positions = detector.getPosition(img, [8, 12, 16], 0, True)
    finger_positions = detector.getPosition(img,[8])
    if finger_positions:
        x1, y1 = finger_positions[0]
    # Draw circles for each finger
    #for i, color in zip(finger_positions, [(0, 255, 0), (255, 0, 0), (125, 50, 255)]):
        #cv2.circle(img, i, 7, color, cv2.FILLED)

    index = int(detector.index_finger_up(img))
    ring = int(detector.ring_finger_up(img))
    middle = int(detector.middle_finger_up(img))
    little = int(detector.little_finger_up(img))
    all = str(index) + str(middle) + str(ring) + str(little)

    #print(finger_positions) to print the raw coords of where the index finger is

    cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (0, 120, 120), 2)


    # Check which fingers are up
    if all == "1000" : #movement of cursor
        cv2.putText(img, "moving " , (0, 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1)
        mx = np.interp(x1,(frameR,width-frameR),(0,wscreen))
        my = np.interp(y1,(frameR,height-frameR),(0,hscreen)) # raw coordinates for x and y scaled to the screen

        clocX = plocX + (mx - plocX) / smoothening
        clocY = plocY + (my - plocY) / smoothening # smooth coordinates

        cv2.circle(img, (x1,y1), 7, (0,255,0, cv2.FILLED))
        pyautogui.moveTo(wscreen-clocX,clocY)
        plocX,plocY = clocX,clocY
    elif all == "1100" :#left click
        cv2.putText(img, "left click " , (0, 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1)

        pyautogui.click()
    elif all == "1001":#right click
        cv2.putText(img, "right click " , (0, 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255), 1)

        pyautogui.rightClick()

    #frame rate
    cTime= time.time()
    fps = 1 /(cTime-pTime)
    pTime = cTime


    cv2.putText(img,"FPS : " + str(int(fps)),(500,25) , cv2.FONT_HERSHEY_COMPLEX_SMALL , 1 ,(255,255,255),1)

    #display
    cv2.imshow("Hand Tracker",img)
    cv2.waitKey(10)