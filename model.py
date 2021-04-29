
# all_names = [] -- global list, containing the names of all students whose data(sample images) are already present
# all_ids= () --global tuple, containing the ids of all students whose data(sample images) are already present
# students = {} -- global dictionary, containing key: value pairs as :-(id:name)
#                                     - keys :- (unique)id of a student
#                                     - values :- name of syudent , with id "key"
from tkinter import messagebox
import csv
import  os
import re
import datetime

class Model:
    def __init__(self):

        global BASE_DIR
        BASE_DIR = os.path.dirname(os.path.abspath("__file__"))
        self.csv_files_path = os.path.join(BASE_DIR,"attendance")

        self.all_names=[]
        self.all_ids=set()
        self.students={}
        self.setup_lsts()
    
    def setup_lsts(self):

        req_folder = os.path.join(BASE_DIR, "Dataset")
        for f in os.listdir(req_folder):
            
            id= int(re.findall(r"\d+", f)[0])
            name =re.findall("[a-zA-Z]+", f)[0]

            self.all_ids.add(id)
            if (name not in self.all_names):
                self.all_names.append(name)

            self.students[id] = name

 
    def insert_record(self,s_name,s_id):

        self.all_ids.add(s_id)

        if (s_name not in self.all_names):
            self.all_names.append(s_name)

        self.students[s_id] = s_name

    def mark_attendance(self,Id):# mark the attendance in csv file
        today = str(datetime.date.today())
        file_name = today +".csv"
        
        file_name_with_path= os.path.join(self.csv_files_path,file_name)
         
        if (file_name not in os.listdir(self.csv_files_path)): # if today's  attendance's csv file is NOT present
            self.create_csv_file(file_name_with_path)
            
        
        with open(file_name_with_path ,'a') as file:
            fieldnames= ["NAME", "ID"]
            data_to_insert={'NAME':self.students[Id],'ID':Id} 
            csv_writer =csv.DictWriter(file,fieldnames=fieldnames,delimiter='\t')
            csv_writer.writerow(data_to_insert)

        messagebox.showinfo("Attendance marked", "Attendance marked for student '" +self.students[Id]+"' with id "+str(Id))


    def create_csv_file(self,file_name_with_path):               

        with open(file_name_with_path,'w') as file:

            fieldnames= ["NAME", "ID"]
            csv_writer =csv.DictWriter(file,fieldnames=fieldnames,delimiter='\t')
            csv_writer.writeheader()