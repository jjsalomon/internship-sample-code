# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:18:37 2017

@author: jsalomo1
"""

import numpy as np
import cv2
from imutils import face_utils

# import datetime
import imutils
import dlib
import cv2
import math
cap = cv2.VideoCapture('Ali01.m4v')
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('resultBlink.avi',fourcc, 20.0, (640,480))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
blinks = 0
blinkReset = False

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # Detect faces in the grayscale frame
        rects = detector(gray,0)
        # Loop over the face detections
        for rect in rects:
            # Determine the facial landmarks for the face region
            # Then convert the facial landmark (x,y)
            # coordinates to a NumPy array
            shape = predictor(gray,rect)
            shape = face_utils.shape_to_np(shape)
            
#            eyes = shape[36:48]
            eyes = shape[39:40]
            # Coordinates
            # A Top Left
            ATL = shape[37:38]
            # A Bottom Left and Right
            ABL = shape[41:42]
            # Root
            ABR = shape[39:40]
            
            # B Top right
            BTR = shape[44:45]
            # B Bottom Left and Right
            # Root
            BBL = shape[42:43]
            BBR = shape[46:47]
            
            for(x,y) in shape:
                cv2.circle(frame,(x,y),2,(255,0,0),-1)

            # Euclidean Distances - Creating triangles
            # Left Eye
            # A
            AdistanceA = np.linalg.norm(ATL - ABL)
            # B
            AdistanceB = np.linalg.norm(ABL - ABR)
            # C
            AdistanceC = np.linalg.norm(ATL - ABR)
            
            ACosA = ((AdistanceB**2 + AdistanceC**2) - AdistanceA**2)
            AdividerA = 2*(AdistanceB * AdistanceC)
            ACosA = ACosA / AdividerA
            Aangle = math.degrees(math.acos(ACosA))
            
            # Right Eye
            BdistanceA = np.linalg.norm(BTR - BBR)
            BdistanceB = np.linalg.norm(BBL - BBR)
            BdistanceC = np.linalg.norm(BBL - BTR)
            
            BCosA = ((BdistanceB**2 + BdistanceC**2) - BdistanceA**2)
            BdividerA = 2*(BdistanceB * BdistanceC)
            BCosA = BCosA / BdividerA
            Bangle = math.degrees(math.acos(BCosA))
            
            if(Aangle > 22 or Bangle > 22):#            cv2.putText(frame,"Left Eye Angle:"+str(Aangle),(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
#            cv2.putText(frame,"Right Eye Angle:"+str(Bangle),(10,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
#            cv2.putText(frame,"Number of Blinks:"+str(blinks),(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                blinkReset = True
            
            if(blinkReset == True):
                if(Aangle < 18 or Bangle < 18):
                    blinks += 1
                    blinkReset = False



            cv2.imshow('frame',frame)
            out.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()