# -*- coding: utf-8 -*-

import cv2
import dlib
import math
import os
import re
import fnmatch
import numpy as np
from imutils import face_utils
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('facialAnalyzerResult.avi',fourcc, 20.0, (640,480))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
blinks = 0
blinkReset = False
angleList = []
peaks = 0
troughs = 0
Duration = 0

imageArray = []
sorted_imageArrayNames = []
image_paths = "\\jelo\\"
path = os.getcwd() + image_paths
unsorted_imageArrayNames = fnmatch.filter(os.listdir(path), '*.jpg')

for i in range(len(unsorted_imageArrayNames)):
    imageArray.append(int(unsorted_imageArrayNames[i].strip('.jpg')))
    imageArray.sort(key=int)
for i in range(len(imageArray)):
    sorted_imageArrayNames.append(str(imageArray[i]) + ".jpg")
for i in range(0,len(sorted_imageArrayNames)):
    print(sorted_imageArrayNames[i])
    frame = cv2.imread(path + sorted_imageArrayNames[i])
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    out.write(frame)
out.release()