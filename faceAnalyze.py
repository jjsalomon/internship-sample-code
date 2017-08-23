''' Video Facial Analyzer Module
        Needs hachoir to be installed
        pip install -U hachoir3
    Developed By: jsalomo1
'''
import cv2
import dlib
import math
import os
import threading
import fnmatch
import numpy as np
from imutils import face_utils
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
import logging

class FacialAnalyzer():
    def __init__(self):
        self.LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        logging.basicConfig(filename="logfiles\\facialanalyzer.log",
                                 level = logging.DEBUG,
                                 format = self.LOG_FORMAT,
                                 filemode = 'w')
        self.logger = logging.getLogger()
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.blinks = 0
        self.blinkReset = False
        self.angleList = []
        self.peaks = 0
        self.troughs = 0
        self.duration = 0
        self.userId = 0
        self.username = ""
        self.logger.info("Facial Analyzer Module Instantiated")
        self.out = cv2.VideoWriter("\\recordings_video\\"+self.user+'\\facialAnalyzerResult.avi',self.fourcc, 20.0, (640,480))
        
    def beginAnalysisThread(self,user,userId,dbh):
        try:
            self.dbh = dbh
            self.username = user
            self.userId = userId
            self.logger.info("Analysis Thread has Begun(user:{0}, userId:{1},database instance:{2})".format(self.username,self.userId,dbh))
            self.Thread = threading.Thread(target=self.dataExtractVideoRecording,args=("test",))
            self.Thread.start()
            return True
        except:
            self.logger.error("Facial Analysis Has Failed(user:{0}, userId:{1},database instance:{2})".format(self.username,self.userId,dbh))
            return False
        
    def calculateAngle(self,pointA, pointB, pointC):
        try:
            # Calculate Euclidean Distance
            distanceA = np.linalg.norm(pointB - pointC)
            distanceB = np.linalg.norm(pointA - pointC)
            distanceC = np.linalg.norm(pointA - pointB)
            
            # using Cos to calculate the required angle.
            dividerA = 2*(distanceB * distanceC)
            cosA = ((distanceB**2 + distanceC**2) - distanceA**2) / dividerA
            angleResult = math.degrees(math.acos(cosA))
            
            return angleResult
        except Exception as e:
            self.logger.error("Failed to calculate Angle of A".format(e))
            return False
            
    def blinkExtractor(self,shape):
        try:
            # Left Eye Points
            ATL = shape[37:38]
            ABL = shape[41:42]
            ABR = shape[39:40]
            # Right Eye Points
            BTR = shape[44:45]
            BBL = shape[42:43]
            BBR = shape[46:47]
            
            # Left Eye Angle
            angleA = self.calculateAngle(ABR,ATL,ABL)
            # Right Eye Angle
            angleB = self.calculateAngle(BBL,BTR,BBR)
                    
            if(angleA > 22 or angleB > 22):
                self.blinkReset = True
                
            if(self.blinkReset == True):
                if(angleA < 18 or angleB < 18):
                    self.blinks += 1
                    self.blinkReset = False
            return True
        except:
            self.logger.error("Blink Extractor Function Failed(ATL{0}, ABL{1},ABR{2})".format(ATL,ABL,ABR))
            return False

        
    def jawAngleExtractor(self,shape):
        try:
            # Facial Points for Jaw
            jawPointLeft = shape[3:4]
            nosePointMid = shape[27:28]
            jawPointBottom = shape[8:9]
            
            jawAngle = self.calculateAngle(jawPointLeft,jawPointBottom,nosePointMid)
        
            self.angleList.append(str(jawAngle))
            return True
        except:
            self.logger.error("Jaw Angle Extractor Failed")
            return False
        
    def peaksTroughsExtractor(self):
        try:
            # Float conversion
            # Array to hold the jaw angles
            floatArray = [float(i) for i in range(len(self.angleList))]
            # Calculating Peaks
            peaksArray = [i for i in range(1,len(floatArray)-1) if(floatArray[i] > floatArray[i-1] and floatArray[i] > floatArray[i+1])]
            self.peaks = len(peaksArray)
            # Calculating Troughs
            troughsArray = [i for i in range(1,len(floatArray)-1) if(floatArray[i] < floatArray[i-1] and floatArray[i] < floatArray[i+1])]
            self.troughs = len(troughsArray)
            self.logger.info("Analysis Result: Peaks{0}, Troughs{1}".format(self.peaks,self.troughs))
        except:
            self.logger.error("Peaks & Troughs Data Extractor Failed")
            return False
        
    def insertAnalyzeData(self):
        try:
            peakspermin = (self.peaks / self.duration) * 60
            troughspermin = (self.troughs / self.duration) * 60
            blinkspermin = (self.blinks / self.duration) * 60
            #self.dbh.insert_videorecordings(self.userId,self.blinks,self.peaks,self.troughs,
            #                                blinkspermin,peakspermin,troughspermin,self.Duration,"Insert")
            self.logger.info("Data has been inserted into the Database")
            self.resetValues()
            return True
        except:
            self.logger.error("Insert Analyze Failed")
            return False
        
    def resetValues(self):
        try:
            self.peaks,self.troughs,self.blinks,self.duration = 0,0,0,0
            self.blinkReset = False
            self.angleList.clear()
            self.userId = 0
            self.username = ""
            self.logger.info("Analysis values has been reset")
            return True
        except:
            self.logger.error("Reset Failed")
            return False
        
    def dataExtractVideoRecording(self,test):
        try:
            # Read in the images and sort them
            image_paths = "\\recordings_video\\"+self.username+"\\"
            self.logger.info("Image Path:{0}".format(image_paths))
            path = os.getcwd() + image_paths
            unsorted_imageArrayNames = fnmatch.filter(os.listdir(path), '*.jpg')
            imageArray = [int(unsorted_imageArrayNames[i].strip('.jpg')) for i in range(len(unsorted_imageArrayNames))]
            imageArray.sort(key=int)
            sorted_imageArrayNames = [str(imageArray[i])+".jpg" for i in range(0,len(imageArray))]
            self.logger.debug("Pass !")
            for i in range(0,len(sorted_imageArrayNames)):
                frame = cv2.imread(path + sorted_imageArrayNames[i])
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                # Detect faces in the grayscale frame
                rects = self.detector(frame,0)
                # Loop over the face detections
                for rect in rects:
                    # Determine the facial landmarks for the face region
                    # Then convert the facial landmark (x,y)
                    # coordinates to a NumPy array
                    shape = self.predictor(gray,rect)
                    shape = face_utils.shape_to_np(shape)
                    self.blinkExtractor(shape)
                    self.jawAngleExtractor(shape)
                    #cv2.putText(frame,"Number of Blinks:"+str(self.blinks),(10,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
                    self.out.write(frame)
            # Finish the recording
            self.out.release()
            file = os.getcwd() +'\\output.avi'
            parser = createParser(file)
            metadata = extractMetadata(parser)
            durationString = [i for i in metadata.exportPlaintext() if "Duration" in i]
            if not durationString:
                self.logger.info("No Duration Value")
                return False
            else:
                self.duration = float(durationString[0][12:14] + "." + durationString[0][19:20])
                self.logger.info("Duration{0}, Blinks{1}".format(self.duration,self.blinks))
                self.peaksTroughsExtractor()
                self.insertAnalyzeData()
                self.logger.info("Video Analysis Completed")
                return True
        except:
            self.logger.error("Root Data Extraction Method Failed")
            return False
    
    
    