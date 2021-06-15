import mediapipe as mp
# install (if any problem in installing mediapipe
# x86: vc_redist.x86.exec-64bit
# x64: vc_redist.x64.exe-32 bit
import cv2
import time
import handdetection as hp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
cap=cv2.VideoCapture(0)
cap.set(3,650)
cap.set(4,480)
detector=hp.handetector(detectionCon=0.7,trackcon=0.5,max_num_hands=1,)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
minvol=volrange[0]
maxvol=volrange[1]
area=0
while True:
    success,img=cap.read()
    img=detector.findhands(img)
    lmlist,bbox=detector.findpos(img,draw=True)
    vol=0
    if len(lmlist) !=0:

        # Filter based on size
        area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])




        #print(lmlist[4],lmlist[8])
        cv2.circle(img, (lmlist[4][1], lmlist[4][2]), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (lmlist[8][1], lmlist[8][2]), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(lmlist[4][1], lmlist[4][2]),(lmlist[8][1], lmlist[8][2]),(255,0,255),3)
        cx,cy= (lmlist[8][1] + lmlist[4][1]) //2 ,(lmlist[8][2]+lmlist[4][2])//2
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        length=math.hypot(lmlist[8][1]-lmlist[4][1],lmlist[8][2]-lmlist[4][2])
        #length1=np.interp(area ,[])
        if(length<50):
            cv2.circle(img, (cx, cy), 15, (0,255,0), cv2.FILLED)
        area=area/250
        #print(length,area)
        if(area==0):
            area=1
        if(length<area+20 and length >20):
            #vol=(length-20)/int((area)/65) - 65
            vol=np.interp(length,[20,area+20],[0,100])

            #reduce resolution
            smoothness=3
            volper=smoothness*round(vol/smoothness)
            #check finger up
            fingers=detector.fingersup()
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(vol / 100, None)
                print(fingers)



    cv2.imshow("Image",img)

    cv2.waitKey(1)