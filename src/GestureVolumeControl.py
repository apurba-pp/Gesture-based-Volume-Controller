import cv2
import time
import mediapipe as mp
import Handtrackmodule as htm
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume 

wCam, hCam = 648, 480



cTime = 0 
cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = (volume.GetVolumeRange())

minVol= volRange[0]
maxVol= volRange[1]

vol=0
volBar=400
volPer=0


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0:
        #print(lmList[4], lmList[8])
        #print(lmList[0], lmList[1])

        x1, y1= lmList[4][1], lmList[4][2]
        x2, y2= lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2


        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2,y2),(255,0,255), 3)
        cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)

        x3, y3= lmList[3][1], lmList[3][2]
        #x4, y4= lmList[1][1], lmList[1][2]
        #dx, dy = (x3+x4)//2, (y3+y4)//2
        

        cv2.circle(img, (x3,y3), 5, (0,120,255), cv2.FILLED)
        #cv2.circle(img, (x1,y1), 5, (0,120,255), cv2.FILLED)
        cv2.line(img, (x3, y3), (x1,y1),(0,120,255), 3)
        #cv2.circle(img, (dx,dy), 15, (255,0,255), cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        lengthRef=math.hypot(x1-x3,y1-y3)
        print(length, lengthRef)

        # Hand Range 70-250
        # Volume Range -65-0
        relativeLenth= 50

        vol = np.interp(length, [70*(lengthRef/relativeLenth),250*(lengthRef/relativeLenth)],[minVol, maxVol])
        volBar = np.interp(length, [70*(lengthRef/relativeLenth),250*(lengthRef/relativeLenth)],[400, 150])
        volPer = np.interp(length, [70*(lengthRef/relativeLenth),250*(lengthRef/relativeLenth)],[0, 100])
        #print(int(length),vol)

        volume.SetMasterVolumeLevel(vol, None)

        if length<70:
            cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)


    cv2.rectangle(img, (50, 150), (85, 400), (255,100,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%' , (30,450), cv2.FONT_HERSHEY_PLAIN, 3, (255,100,0), 3)
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{int(fps)}' , (10,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,100,0), 3)
        
    cv2.imshow("Image", img)
    cv2.waitKey(1)
