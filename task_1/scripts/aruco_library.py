#!/usr/bin/env python3
############## Task1.1 - ArUco Detection ##############

import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time

def detect_ArUco(img):
    global ids1, ids2
    Detected_ArUco_markers = {}
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoParameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=arucoParameters)
    if np.all(ids != None):
        display = aruco.drawDetectedMarkers(img, corners)
        for corner,id in zip(corners,ids):
            id1=int(id)
            Detected_ArUco_markers[id1]=corner[0]
    print(Detected_ArUco_markers)
    return Detected_ArUco_markers

def Calculate_orientation_in_degree(Detected_ArUco_markers):
    ArUco_marker_angles = {}
    for key,value in Detected_ArUco_markers.items():
        x1=value[0][0]
        x2=value[1][0]
        x3=value[2][0]
        x4=value[3][0]
        y1=value[0][1]
        y2=value[1][1]
        y3=value[2][1]
        y4=value[3][1]

        tx=int((x1+x2)/2)
        ty=int((y1+y2)/2)

        cx = int(((x1 + x3) / 2))
        cy = int(((y1 + y3) / 2))

        l=math.sqrt((math.pow((tx-cx),2))+(math.pow((ty-cy),2)))

        tx=tx-cx
        ty=ty-cy

        ax=l
        ay=0

        a=np.array([0,0])
        b=np.array([ax,ay])
        c=np.array([tx,ty])

        ba=b-a
        ca=c-a

        cosine_angle = np.dot(ba,ca) / ( np.linalg.norm(ba) * np.linalg.norm(ca))
        if(ty>0):
            
            angle = (360-math.floor(np.degrees(np.arccos(cosine_angle))))
            ArUco_marker_angles[key]=angle
        else:
            
            angle = math.floor(np.degrees(np.arccos(cosine_angle)))
            ArUco_marker_angles[key]=angle
    print(ArUco_marker_angles)
    return ArUco_marker_angles

def mark_ArUco(img,Detected_ArUco_markers,ArUco_marker_angles):
    font = cv2.FONT_HERSHEY_SIMPLEX
    for (key,value),(id,angle) in zip(Detected_ArUco_markers.items(),ArUco_marker_angles.items()):
        x1=value[0][0]
        x2=value[1][0]
        x3=value[2][0]
        x4=value[3][0]
        y1=value[0][1]
        y2=value[1][1]
        y3=value[2][1]
        y4=value[3][1]
        tx=int((x1+x2)/2)
        ty=int((y1+y2)/2)
        cx = int(((x1 + x3) / 2))
        cy = int(((y1 + y3) / 2))
        img=cv2.circle(img,(x1,y1),4,(125,125,125),-1)
        img=cv2.circle(img,(x2,y2),4,(0,255,0),-1)
        img=cv2.circle(img,(x3,y3),4,(180,105,255),-1)
        img=cv2.circle(img,(x4,y4),4,(255,255,255),-1)
        img=cv2.circle(img,(cx,cy),6,(0,0,255),-1)
        img=cv2.line(img,(cx,cy),(tx,ty),(255,0,0),5)
        img=cv2.putText(img,str(key), (int(cx+20),int(cy+20)), font,1, (0,0,255), 2, cv2.LINE_AA)
        img=cv2.putText(img,str(angle), (int(x4-50),int(y4-30)), font,1, (0,255,0), 2, cv2.LINE_AA)
    return img
