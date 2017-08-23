# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 09:47:40 2017

@author: jsalomo1
This script runs the facial land mark detection of the user
"""
# imutils setup
from imutils.video import VideoStream
from imutils import face_utils

import datetime
import imutils
import time
import dlib
import cv2
import numpy as np
import threading
import os
import random

# Single Instance
class FacialDetection():
    
    __instance = None
    
    @staticmethod
    def getInstance():
        # If no instance has been created
        # Create the instance
        if FacialDetection.__instance == None:
            FacialDetection()
        return FacialDetection.__instance  
    
    def __init__(self):
        if FacialDetection.__instance != None:
            print("Returning facial rec single instance")
        else:
            FacialDetection.__instance = self
            print('[BOOTING]: Facial Detection Module')
            # Initializing dlib's face detector (HOG-based)
            # and then create the facial landmark predictor
            print("[INFO] loading facial landmark predictor...")
            self.detector = dlib.get_frontal_face_detector()
            self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
            # Initialize the video stream and allow the camera sensor to warm up
            print("[INFO] camera sensor warming up...")
            #self.vs = VideoStream().start()
            self.cap = cv2.VideoCapture(0)
            time.sleep(2.0)
            self.endRec = False
            self.containsFace = False
            self.user = ""
        
        
    def initVideoWriters(self,username):
        #os.chdir('recordings_video')
        #os.chdir(self.user)
        time = datetime.datetime.now()
        AVI_FILENAME = time.strftime("%d-%m-%y_%H-%M") + ".avi"
        PATH = 'recordings_video/' + self.user + '/' + AVI_FILENAME
        # Define codec and create VideoWriter Object
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        self.out = cv2.VideoWriter(PATH,self.fourcc, 20.0, (640,480))
        #os.chdir('../..')
        self.endRecordFile = False
        
    def calibrationVideo(self):
        while not self.containsFace:   
            val,currFrame = self.generate()
                
            yield (b'--frame\r\n' 
                   b'Content-Type: image/jpeg\r\n\r\n' + currFrame + b'\r\n')


    def generate(self):
        frame = self.cap.read()

        gray = cv2.cvtColor(frame[1],cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale frame
        rects = self.detector(gray,0)
        # Loop over the face detections
        for rect in rects:
            # Determine the facial landmarks for the face region
            # Then convert the facial landmark (x,y)
            # coordinates to a NumPy array
            shape = self.predictor(gray,rect)
            shape = face_utils.shape_to_np(shape)
    			# store shape into a file
            # and draw on the image
            for(x,y) in shape:
                cv2.circle(frame[1],(x,y),1,(0,0,255),-1)
            
        ret,jpeg = cv2.imencode('.jpg',frame[1])
        
        if len(rects) > 0:
            self.containsFace = True
        else:
            self.containsFace = False
        
        return frame[1], jpeg.tobytes()
                
    def startRecordLoop(self):
        Looper = True
        while Looper == True:
            # Stream frames
            frame, jpeg = self.generate()
            self.out.write(frame)
            
            if (self.endRecordFile == True):
                self.out.release()
                self.cap.release() 
                Looper = False
                return 0
    
    # This breaks the loop above
    def endRecord(self):
        self.endRecordFile = True
        
    # Starts the thread.
    def triggerRecord(self,username):
        self.user = username
        self.initVideoWriters(self.user)
        self.recordThread = threading.Thread(target = self.startRecordLoop)
        self.recordThread.start()
        
    
            