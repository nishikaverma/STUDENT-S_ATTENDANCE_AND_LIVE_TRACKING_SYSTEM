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


class controller:
    def __init__(self):

        self.face_cascades = cv2.CascadeClassifier(
            '/home/nishi/Desktop/MAJOR PROJECT/New_sys/haarcascades/haarcascade_frontalface_default.xml')

        #self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.trainingOngoing = False
        self.sample_count = 0

####################################  FACE DETECTION  ###################################################################

    # capturing the frames i.e. display the video
    def Video_capture(self, s_id=None, s_name=None):

        self.capture = cv2.VideoCapture(0)

        while True:
            ret, frame = self.capture.read(0)
            frame = self.Face_detector(frame, s_id, s_name)

            font = cv2.FONT_HERSHEY_SIMPLEX
            if self.trainingOngoing != True:
                cv2.putText(frame, "press 'ESC' for stopping the tracking ",
                            (10, 17), font, 1, (0, 255, 255), 1, cv2.LINE_4)
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

        #Img = img.copy()
        found = self.face_cascades.detectMultiScale(
            img, scaleFactor=1.2, minNeighbors=3)

        # print('found fas are :', found)

        if (found != ()):
            for (x, y, w, h) in found:
                # Draw a rectangle around the faces
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                #--------------code for taking sample images for training the model ---------#
                if self.trainingOngoing == True:
                    self.Store_images(img, x, y, w, h, s_id, s_name)

                #-------------------------------------------------------------------------------#

        else:
            print("NO face found!!")

        return img

########################################################################################################

    # --------------- code for taking and storing sample images for training the model:----------------
    def Store_images(self, img, x, y, w, h, s_id, s_name):

        Img = img.copy()
        gray = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)

        folder_name = s_name+str(s_id)
        folder_name_path = folder_name+"/"

        BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
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

    def getImagesAndLabels(self):

        BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
        req_path = os.path.join(BASE_DIR, "Dataset")

        imagePaths = []
        for folder in os.listdir(req_path):
            temp_path = os.path.join(req_path, folder)

            for sample_img in os.listdir(temp_path):
                imagePaths.append(os.path.join(temp_path, sample_img))

        print(imagePaths)
        faceSamples = []
        Ids = []
        for i in imagePaths:
            pilImage = Image.open(i)
            imageNp = np.array(pilImage, 'uint8')
            faces = self.face_cascades.detectMultiScale(imageNp)
            # --->Id=int(os.path.split(imagePath)[-1].split(".")[1])
            if (faces != ()):
                for (x, y, w, h) in faces:
                    faceSamples.append(imageNp[y:y+h, x:x+w])
                    # -->Ids.append(Id)
        return faceSamples, Ids
