
# all_names = [] -- global list, containing the names of all students whose data(sample images) are already present
# all_ids= () --global tuple, containing the ids of all students whose data(sample images) are already present
# students = {} -- global dictionary, containing key: value pairs as :-(id:name)
#                                     - keys :- (unique)id of a student
#                                     - values :- name of syudent , with id "key"


from pyexcel_ods3 import save_data
from pyexcel_ods import get_data
from collections import OrderedDict
import json
import pyexcel as pe
from io import StringIO

class Model:

    def __init__(self):

        self.all_names=[]
        self.all_ids=set()
        self.students={}

        self.setup_lsts()

        self.sheet = pe.get_sheet(file_name="Student_data.ods")
    
    def setup_lsts(self):
        data = dict(get_data("Student_data.ods"))# got data in the form of JSON object 
        
        for v in data.values():
            for record in v[1:]:
                if (record):
                    if record[0] not in self.all_names:
                        self.all_names.append(record[0])
                    self.all_ids.add(record[1])
                    self.students[record[1]] = record[0]
        
        print("______________________record loaded form excel sheet are: -------------------")
        print(self.all_ids)
        print(self.all_names)
        print(self.students)
        print("_____________________________________________________________________________")


    def insert_record(self,s_name,s_id):
        try:
            print("BEFORE UPDATE : ")
            print(self.sheet)

            self.sheet.row += [s_name,s_id]
            self.sheet.save_as("Student_data.ods")

            print("AFTER UPDATE :")
            print(self.sheet)

            self.update_lsts(s_name,s_id)
            return True
        except Exception as e:
            print(e)
            return False
    
    def update_lsts(self,s_name,s_id):

        self.all_ids.add(s_id)
        if (s_name not in self.all_names):
            self.all_names.append(s_name)

        self.students[s_id] = s_name
        
        print("UPDATED LISTS ARE:")
        print(self.all_ids)
        print(self.all_names)
        print(self.students)
        