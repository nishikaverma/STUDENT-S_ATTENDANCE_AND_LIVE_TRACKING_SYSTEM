STUDENT ATTENDANCE SYSTEM AND  LIVE TRACKING 


![main_window](https://user-images.githubusercontent.com/51054631/116808268-7cd78100-ab55-11eb-8067-2c7b24e60d7c.png)

![taking_data_set](https://user-images.githubusercontent.com/51054631/116808316-c45e0d00-ab55-11eb-883b-1010591d1ad4.png)

![face_detection_reco_racking](https://user-images.githubusercontent.com/51054631/116808282-98db2280-ab55-11eb-9dd1-d726286d2308.png)

![attendance_marking](https://user-images.githubusercontent.com/51054631/116808354-eeafca80-ab55-11eb-8f24-c1b4366c2f43.png)






​​​​TECHNOLOGY USED ​​​​

The system is implemented using Python Programming Language.
​It makes use of :
  ​Face Detection 
  ​Face Recognition

with the help of Python's libraries such as :

​CV2 : An openCV library for Image processing .

​NUMPY : For computing, processing and performing various  operations on arrays (as an image is an array of pixels values) .

​MATPLOTLIB, PIL : for capturing, opening and saving the image  set as a file.

​Tkinter : for making the graphical user interface of the application.

​CSV : for storing attedance data in a CSV file formate.

​OS : for performing operations over system paths .

​re, datetime  : for other internal computations.


​​​​​SYSTEM FLOW CONTROL ​​​​​​

​ The system is built upon MVC design  architecture

​   model.py ------------>  controller.py  -----------> views.py   ​

​model.py :  It manages all the updations and maintainance (attendance marking, attendanec file creation, etc.) of CSV files.  

​controller.py :  It takes all the event requests from "views.py" , process it, and sends the response back .Also forwards the requests to model.py, if required, accepts & transfers the  response back to views.py .

​views.py : Contains all the GUI (Front end) of app. Takes all the requests.

​​​​​​​ALGORITHM ​​​​​​​​​

1. Object(face) tracking on the video (face detection +tracking)
2. Capturing  face samples and storing it.
3.  Creating and training face detection "model"  (.yml file)
4.  Face detection  + Face recognization
5.  Attendance marking (csv file updation)



    1. Object(face) tracking on the video (face detection +tracking):
      
    • As soon as the tracking is “on”, the system detects object (here faces) on the video frame and faces are detected, which are then tracked on the screen.
    • Here, since NO sample images are given to the system as a refrence for face recognization, the system will only detect (and track) faces, but not recognizes them.


    2. Capturing  face samples and storing it:
       
    • For making the system to be able to  recognize faces, sample data should be given. Thus, the system will capture  some fixed (constant int) number of facial image samples of each student, whose face is needed to be recognized.


    3. Creating and training face detection "model" (.yml file):
       
    • Once sample images are stored in the system, a face recognization model (a .yml file) is then created, and trained with the given sample images, simaltaneously, so as to recognize faces on screen.
       
    4. Face detection +Face recognization:
       
    • So, now when the video is ON, the system is able to detect as well as recognize faces on the screen.
    • The recognised student’s faces will be displayed with their name on the video frame.


    5. Attendance marking (csv file updation):
      
    • Once the faces are being successfully recognized, the presence of recognised faces are tracked on the video frame for a perticular amount of time .
      
    • Thus, the amount of time an object appears on the video frame is called as Dwell time of an object.
      
    • If a face is beig recognized for a fixed amount of time (implicit in the system), then the face(corrusponding student) is marked as “present”.
      
    • The attendance data is then simaltaneously updated in the CSV file. 
      
      

​ Face Detection : 

HARCASCADE CLASSIFIERS (which internally uses "FEATURE MATCHING algo") is used for face detection.

By passing 'cascade'(series) of 'classifiers' ('predefined features' which are nothing but group of arrays of 'float values' i.e. a matrix, denoting the grey color point  of an image.

As, an image is nothing but  a matrix of floating point numbers.

​Face Recognization :

LBPH recognization algorithm is used for facial recognization.

It  compares the input facial image with all facial images existing inside the dataset, with the aim to find the image that best matches that face.

It is basically a 1xN comparison.




