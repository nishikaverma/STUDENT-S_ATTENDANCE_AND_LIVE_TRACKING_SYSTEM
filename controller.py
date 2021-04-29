# Algorithm for "STORING" and "Training" the model :-
# {via - def Capture image()} ==>
#       step 1) The data(images of students) will be collected, and stored inside "Dataset" folder.
#       step 2) Training our 'model' with the dataset(collected images), stored inside the "Dataset" folder.
# {Via - def trainer ()} ==>
#       step 3) The 'trained model'(.yml file ) is then stored inside the "Model" folder.


# all_names = [] -- global list, containing the names of all students whose data(sample images) are already present
# all_ids= () --global tuple, containing the ids of all students whose data(sample images) are already present
# students = {} -- global dictionary, containing key: value pairs as :-(id:name)
#                                     - keys :- (unique)id of a student
#                                     - values :- name of syudent , with id "key"


import os
import cv2
from PIL import Image
import numpy as np
import pickle
import re
import model
import datetime


class controller:
    def __init__(self):

        global BASE_DIR
        global yml_path

        BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
        path = os.path.join(BASE_DIR, 'haarcascades',
                            'haarcascade_frontalface_default.xml')
        self.face_cascades = cv2.CascadeClassifier(path)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        yml_path = os.path.join(BASE_DIR, "Model", "trained_model.yml")
        #font = cv2.FONT_HERSHEY_SIMPLEX
        self.yml_exists = False
        self.trainingOngoing = False
        self.sample_count = 0
        

        self.obj_model= model.Model()


    def face_recognizer(self):
        
        if os.path.exists(yml_path):
            self.recognizer.read('Model/trained_model.yml')
            self.yml_exists = True
            
            self.predicted=[] # contains all the face id's we have tracked/recognized
            self.dtime =dict() # will hold the value of current date time for a face
            self.dwell_time= dict() # will contain dwell time of a face (in sec)
            self.track=dict()
        
        self.Video_capture()
####################################  FACE DETECTION & REGIATION ##############################

    # capturing the frames i.e. display the video
    def Video_capture(self, s_id=None, s_name=None):

        self.capture = cv2.VideoCapture(0)

        while True:
            ret, frame = self.capture.read(0)

            frame = self.Face_detector(frame, s_id, s_name)

            if self.trainingOngoing != True:
                cv2.putText(frame, "press 'ESC' for stopping the tracking ",
                            (10, 17), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_4)
            cv2.imshow("Face_detection", frame)

            #--------------code for taking sample images for training the model ---------#
            if self.trainingOngoing == True:

                if self.sample_count > 50:  # taking only 50 sample image per person
                    break
            #-----------------------------------------------------------------------------#

            else:
                if (cv2.waitKey(1) == 27):  # i.e. if Esc key is pressed
                    break
        self.Video_distroy()

    def Video_distroy(self):
        self.capture.release()
        cv2.destroyAllWindows()
        print("Window distroyed!")

    def Face_detector(self, img, s_id, s_name):  # detects "face" on video frame


        found = self.face_cascades.detectMultiScale(
            img, scaleFactor=1.2, minNeighbors=3)

        if (found != ()):
            for (x, y, w, h) in found:
                # Draw a "rectangle" around the faces, AND "rectangle with name " for recognized faces.
                
                if self.yml_exists == True:
                    
                    gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    Id, conf = self.recognizer.predict(gray[y:y+h, x:x+w])
                    self.dwell_time_calculator(Id)

                    cv2.rectangle(img, (x, y),
                                  (x+w, y+h), (0, 255, 0), 2)
                    NAME= self.obj_model.students[Id]
                    cv2.putText(img, NAME, (x, y-40),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
                cv2.rectangle(img, (x, y),
                              (x+w, y+h), (0, 255, 0), 2)

                #--------------code for taking sample images for training the model ---------#
                if self.trainingOngoing == True:
                    self.Store_images(img, x, y, w, h, s_id, s_name)
                #-------------------------------------------------------------------------------#
        else:
            print("NO face found!!")
        return img


    def dwell_time_calculator(self,Id):
        if Id not in self.predicted: # when face is detected for thre 1st time
            self.track[Id]=False
            self.predicted.append(Id)
            self.dtime[Id]= datetime.datetime.now()
            self.dwell_time[Id]=0


        elif self.track[Id]==False:
            self.current_time =datetime.datetime.now()
            self.old_time = self.dtime[Id]
            time_diff = self.current_time-self.old_time
            self.dtime[Id]= datetime.datetime.now()
            sec = time_diff.total_seconds()
            self.dwell_time[Id] += sec            

            if self.dwell_time[Id] >= 10:

                self.mark_attendance(Id)        
                self.track[Id] =True  

        print(self.dwell_time) 

########################################################################################################

    # --------------- code for taking and storing sample images for training the model:----------------
    def Store_images(self, img, x, y, w, h, s_id, s_name):

        Img = img.copy()
        gray = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)

        folder_name = s_name+str(s_id)
        folder_name_path = folder_name+"/"

        req_path = os.path.join(BASE_DIR, "Dataset", folder_name_path)
        if not os.path.exists(req_path):
            os.mkdir(req_path)

        cv2.imwrite(req_path + folder_name + "_" + str(self.sample_count) + ".jpg",
                    gray[y:y + h, x:x + w])

        print("Image number "+str(self.sample_count) + " captured")

        self.sample_count = self.sample_count + 1

    # ----------------------------------------------------------------------------------------------------
    def trainer(self):

        faces, Ids = self.getImagesAndLabels()
        
        self.recognizer.train(faces, np.array(Ids))
        self.recognizer.save("Model/trained_model.yml")
        if not os.path.exists(yml_path):
            return False

        return True

    def getImagesAndLabels(self):

        req_path = os.path.join(BASE_DIR, "Dataset")

        imagePaths = []
        for folder in os.listdir(req_path):
            temp_path = os.path.join(req_path, folder)

            for sample_img in os.listdir(temp_path):
                imagePaths.append(os.path.join(temp_path, sample_img))

        print("All image paths are :- ", imagePaths)

        faceSamples = []
        Ids = []
        for img_path in imagePaths:
            pilImage = Image.open(img_path)
            imageNp = np.array(pilImage, 'uint8')
            faces = self.face_cascades.detectMultiScale(imageNp)

            # since a face will always be uniquely Identified(ID) by a "id" formate :-
            unique_id_name = os.path.split(
                img_path)[-1].split(".")[0].split("_")[0]

            #print("uniq id name is : ", unique_id_name)

            res = re.findall(r"\d+", unique_id_name)
            #print("digit in name is ; ", res)
            unique_id = int(res[0])

            if (faces != ()):
                for (x, y, w, h) in faces:

                    faceSamples.append(imageNp[y:y+h, x:x+w])
                    Ids.append(unique_id)
        #print("face DAmples are :--  ", faceSamples)
        #print("IDs (lables are): --  ", Ids)
        return faceSamples, Ids

    def insert_record(self,s_name,s_id):
        #updating lists
        self.obj_model.insert_record(s_name,s_id)

    def mark_attendance(self,Id):
        print("Attendance of student"+ str(Id) +"has marked")
        