# -*- coding: utf-8 -*-
import face_recognition
import threading
import os
import cv2
from loggerhelpers import LoggerHelper

class FacialRecognizer():
    def __init__(self):
        self.user_images = []
        self.user_face_encoding = []
        self.new_images_path = str(os.getcwd()+"/files/image_cache/newer_images/")
        self.old_images_path = str(os.getcwd()+"/files/image_cache/older_images/")
        self.username = ""
        lh = LoggerHelper().getInstance()
        self.logger = lh.createLoggerWorker("facerecognizer","DEBUG",2)
        self.logger.info("User Face Recognizer Instantiated")
        print("Facial Recognizer Instantiated")
    def beginUserRecognizerThread(self,username):
        try:
            self.username = username
            self.Thread = threading.Thread(target=self.recognizeImages)
            self.Thread.start()
        except Exception as e:
            self.logger.error("Thread Failed To Start:{0}".format(e))
            
    # This class loads images and creates an encoder.
    def createImageEncoders(self,image_path):
        try:
            # Load image names
            userImageName = self.username+".jpg"
            # Load Actual Images
            userImage = face_recognition.load_image_file(str(image_path + userImageName))
            # strip off the .jpg extension for the images
            username = self.username
            # Create encoders for the images and add to the array
            user_face_encoding = face_recognition.face_encodings(userImage)[0]
            return userImage, username, user_face_encoding
        except Exception as e:
            self.logger.error("Error at createImageEncoders():{0}".format(e))
    
    # resets values
    def resetValues(self):
        try:
            self.user_images = []
            self.user_face_encoding = []
            self.username = ""
        except Exception as e:
            self.logger.error("Error at resetValues():{0}".format(e))
        
    # This function compares an image with a new image
    def recognizeImages(self):
        try:
            # New Images that have been inserted
            new_image, new_username,new_face_encoding = self.createImageEncoders(self.new_images_path)
            self.logger.debug("new_image:{0},new_username:{1},new_face_encoding:{2}".format(new_image,new_username,new_face_encoding))
            # Older images to compare the new images to
            old_image, old_username,old_face_encoding = self.createImageEncoders(self.old_images_path)
            # Read in a smaller frame of the new images
            small_frame = cv2.resize(new_image,(0,0), fx=0.25,fy=0.25)
            self.logger.debug("Small for "+new_username+":{0}".format(small_frame))
            face_locations = face_recognition.face_locations(small_frame)
            self.logger.debug("Face Locations for "+new_username+":{0}".format(face_locations))
            face_encodings = face_recognition.face_encodings(small_frame,face_locations)
            self.logger.debug("Face Encodings for "+new_username+":{0}".format(face_encodings))
            if len(face_locations) and len(face_encodings) == 0:
                print("We could not recognize"+new_username+"'s face on the image")
            else:
                for face_encoding in face_encodings:
                    self.logger.debug("Pass")
                    match = face_recognition.compare_faces([old_face_encoding],face_encoding)
                    self.logger.debug("Match:{0}".format(match))
                    if match[0]:
                        # take old usernames and compare with new usernames for a match
                        if(new_username in old_username) == True:    
                            name = "We Recognized: "+new_username
                            self.logger.debug("Recognized:{0}".format(name))
                            print(name)
                    else:
                        name = "There was no Match"   
            self.resetValues
            print("Finished")
        except Exception as e:
            self.logger.error("Error at recognizeImages():{0}".format(e))