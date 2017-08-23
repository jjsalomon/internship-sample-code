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
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import os

cap = cv2.VideoCapture('output.avi')
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('resultMouth.avi',fourcc, 20.0, (640,480))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
blinks = 0
blinkReset = False
angleList = []

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

            jawPointLeft = shape[3:4]
            nosePointMid = shape[27:28]
            jawPointBottom = shape[8:9]
            
            for(x,y) in jawPointLeft:
                cv2.circle(frame,(x,y),2,(0,255,0),-1)
            for(x,y) in nosePointMid:
                cv2.circle(frame,(x,y),2,(0,255,0),-1)
            for(x,y) in jawPointBottom:
                cv2.circle(frame,(x,y),2,(0,255,0),-1)
            

            # Euclidean Distances - Creating triangles
            # A
            AdistanceA = np.linalg.norm(nosePointMid - jawPointBottom)
            # B
            AdistanceB = np.linalg.norm(jawPointLeft - nosePointMid)
            # C
            AdistanceC = np.linalg.norm(jawPointBottom - jawPointLeft)
            
            ACosA = ((AdistanceB**2 + AdistanceC**2) - AdistanceA**2)
            AdividerA = 2*(AdistanceB * AdistanceC)
            ACosA = ACosA / AdividerA
            Aangle = math.degrees(math.acos(ACosA))
            
            angleList.append(str(Aangle))
            
            cv2.putText(frame,"Jaw Angle:"+str(Aangle),(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
          
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
file = os.getcwd() +'\output.avi'
parser = createParser(file)
metadata = extractMetadata(parser)
charlist = []
stringlist = []
for line in metadata.exportPlaintext():
    charlist += line
stringlist = ''.join(charlist)
Duration = int(stringlist[19:21])
f = open("results.txt","w")
f.write("Duration:"+ str(Duration)+"\n")
for row in angleList:    
    f.write(row+"\n")
f.close()