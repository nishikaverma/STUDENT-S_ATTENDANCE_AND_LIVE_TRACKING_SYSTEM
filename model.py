
# all_names = [] -- global list, containing the names of all students whose data(sample images) are already present
# all_ids= () --global tuple, containing the ids of all students whose data(sample images) are already present
# students = {} -- global dictionary, containing key: value pairs as :-(id:name)
#                                     - keys :- (unique)id of a student
#                                     - values :- name of syudent , with id "key"

import csv
import  os
import re

class Model:
    def __init__(self):
        global BASE_DIR
        self.all_names=[]
        self.all_ids=set()
        self.students={}
        BASE_DIR = os.path.dirname(os.path.abspath("__file__"))


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

