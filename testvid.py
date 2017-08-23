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
cap = cv2.VideoCapture(0)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")




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
            
            firstPointLeft = shape[0:1]
            nosePointMid = shape[27:28]
            jawPointBottom = shape[8:9]
#            for(x,y) in shape:
#                cv2.circle(frame,(x,y),2,(255,0,0),-1)
#            for(x,y) in firstPointLeft:
#                cv2.circle(frame,(x,y),2,(0,255,0),-1)
#            for(x,y) in nosePointMid:
#                cv2.circle(frame,(x,y),2,(0,255,0),-1)
#            for(x,y) in jawPointBottom:
#                cv2.circle(frame,(x,y),2,(0,255,0),-1)

            cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()