import csv

with open("test.csv",'r') as file:
    csv_reader =csv.DictReader(file)

    # for line in csv_reader:
    #     print(line['nishi'])
    with open("test.csv",'w') as f:

        field1 ={'nishi':"sam",'1':'3','23333':"465"}
        fnames =['nishi','1','23333']
        wr= csv.DictWriter(f,fieldnames=fnames,delimiter='\t')
        
        wr.writeheader()
        wr.writerow(field1)
   


  

# with open("new_csv.csv",'r') as file:
#     csv_reader =csv.reader(file,delimiter='\t')
#     for line in csv_reader:
#         print(line)

  
    # for line in csv_reader:
    #     print(line[2])
    

    # with open("new_csv.csv",'w') as newfile:
    #     csv_writer = csv.writer(newfile,delimiter='\t')
    
    #     for line in csv_reader:
    #         csv_writer.writerow(line)



