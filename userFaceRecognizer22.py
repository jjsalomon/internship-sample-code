# -*- coding: utf-8 -*-
import face_recognition
import threading
import os
import fnmatch
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
            user_image_names = fnmatch.filter(os.listdir(image_path), '*.jpg')
            self.logger.debug("User Image Names:{0}".format(user_image_names))
            # Load Actual Images
            user_images = [face_recognition.load_image_file(str(image_path + user_image_names[i])) for i in range(0,len(user_image_names))]
            self.logger.debug("User Images:{0}".format(user_images))
            # strip off the .jpg extension for the images
            usernames = [user_image_names[i].strip('.JPG') for i in range(0,len(user_images))]
            self.logger.debug("User Names:{0}".format(usernames))
            # Create encoders for the images and add to the array
            user_face_encoding = [face_recognition.face_encodings(user_images[i])[0] for i in range(0,len(user_images))]
            self.logger.debug("User Face Encodings:{0}".format(user_face_encoding))
            return user_images, usernames, user_face_encoding
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
            new_images, new_usernames,new_face_encodings = self.createImageEncoders(self.new_images_path)
            self.logger.debug("New Encoders Created:{0}".format(new_usernames))
            # Older images to compare the new images to
            old_images, old_usernames,old_face_encodings = self.createImageEncoders(self.old_images_path)
            self.logger.debug("Older Encoders Created:{0}".format(old_usernames))
            # Read in a smaller frame of the new images
            for i in range(0,len(new_images)):
                self.logger.debug("Looping for {0}".format(new_usernames[i]))
                self.logger.debug(new_usernames[i]+"'s Image is {0}".format(new_images[i]))
                small_frame = cv2.resize(new_images[i],(0,0), fx=0.25,fy=0.25)
                self.logger.debug("Small for "+new_usernames[i]+":{0}".format(small_frame))
                face_locations = face_recognition.face_locations(small_frame)
                self.logger.debug("Face Locations for "+new_usernames[i]+":{0}".format(face_locations))
                face_encodings = face_recognition.face_encodings(small_frame,face_locations)
                self.logger.debug("Face Encodings for "+new_usernames[i]+":{0}".format(face_encodings))
                if len(face_locations) and len(face_encodings) == 0:
                    print("We could not recognize"+new_usernames[i]+"'s face on the image")
                else:
                    for face_encoding in face_encodings:
                        match = face_recognition.compare_faces([old_face_encodings],face_encoding)
                        list_match = [list(i) for i in match]
                        self.logger.debug("Match:{0}".format(match))
                        if list_match[0]:
                            self.logger.debug("Index new_usernames:{0}".format(new_usernames[i]))
                            self.logger.debug("older_usernames:{0}".format(old_usernames))
                            # take old usernames and compare with new usernames for a match
                            if(new_usernames[i] in old_usernames) == True:    
                                name = "We Recognized: "+new_usernames[i]
                                self.logger.debug("Recognized:{0}".format(name))
                                print(name)
                        else:
                            name = "There was no Match"   
            self.resetValues
            print("Finished")
        except Exception as e:
            self.logger.error("Error at recognizeImages():{0}".format(e))