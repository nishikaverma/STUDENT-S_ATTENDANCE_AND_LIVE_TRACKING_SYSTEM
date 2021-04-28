# {'sheet1':   [ [col1, col2, col3] ,   --row1
#                [-,-,-],    --row2
#                [],    --row3
#                [],    --row4
#               ]
#   }


from pyexcel_ods3 import save_data
from pyexcel_ods import get_data
from collections import OrderedDict
import json
import pyexcel as pe
from io import StringIO

print("----------------------------------------------------------------------")

#OVERWRITING ROWS
# data = OrderedDict()
# data.update({"Sheet 1": [[1, 2, 3], [4, 5, 6]]}) 
# #data.update({"Sheet 1": [["row 1", "row 2", "row 3"]]})
# save_data("Student_data.ods", data)
# print("data written")


print("----------------------------------------------------------------------")
# PRINTING SHEET (JSON FORMAT)
data = get_data("Student_data.ods") # got data in the form of JSON object 
print(dict(data))
d1= dict(data)
d1.dele

print("----------------------------------------------------------------------")

# PRINTING SHEET (TABLE FORMAT)
sheet = pe.get_sheet(file_name="Student_data.ods")
print(sheet)

print("----------------------------------------------------------------------")

# ADDING A NEW ROW
sheet.row += [12, 11, 10]
sheet.save_as("Student_data.ods")
print(sheet)







# data = [
#     ["nishi1", 1, 3],
#    ["sam", 5, 6]
# ]
# io = StringIO()
# sheet = pe.Sheet(data)
# sheet.save_to_memory("ods", io)

#print(json.dumps(data))

# import csv

# ifile  = open('Student_data.ods', "rb")
# reader = csv.reader(ifile)

# rownum = 0
# for row in reader:
#     # Save header row.
#     if rownum == 0:
#         header = row
#     else:
#         colnum = 0
#         for col in row:
#             print(col)
#             #print '%-8s: %s' % (header[colnum], col)
#             colnum += 1
            
#     rownum += 1

# ifile.close()