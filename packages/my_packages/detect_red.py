from __future__ import print_function
import argparse
import cv2
import numpy as np


#RGB color ranges
red = "RED"
yellow = "YELLOW"
white = "WHITE"


frames_to_avg = 4
    # color Hue Saturation value ranges
    #Colorbands for RED
REDLOW1 = np.array([0, 100, 20])
REDHIGH1 = np.array([10, 255, 255])

REDLOW2 = np.array([160,100,20])
REDHIGH2 = np.array([179,255,255])

    #Colorbands for YELLOW
YEL_LOW = np.array([20, 100, 100])
YEL_HIGH = np.array([30, 255, 255])

    #Colorbands for WHITE
sensitivity = 15
WHITELOW = np.array([0,0,255-sensitivity])
WHITEHIGH = np.array([255,sensitivity,255])

def mask(color, img):

    frame_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    if color == "RED" :
        lower_mask = cv2.inRange(frame_HSV, REDLOW1, REDHIGH1)
        upper_mask = cv2.inRange(frame_HSV, REDLOW2, REDHIGH2)
        full_mask = upper_mask + lower_mask;
        return full_mask
    if color == "YELLOW":
        mask = cv2.inRange(frame_HSV, YEL_LOW, YEL_HIGH)
        return mask
    if color == "WHITE":
        mask = cv2.inRange(frame_HSV, WHITELOW, WHITEHIGH)
        return mask

def maskColor(color,img):
    frame_threshold = mask(color, img)
    res = cv2.bitwise_and(img,img,mask=frame_threshold)
    colorcnts = cv2.findContours(frame_threshold.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]    
    if len(colorcnts)>0:
        color_area = max(colorcnts, key=cv2.contourArea)
        (xg,yg,wg,hg) = cv2.boundingRect(color_area)
        cv2.rectangle(img,(xg,yg),(xg+wg, yg+hg),(0,255,0),2)
    return(res)
