import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import controller


def start_gui():
    root = tk.Tk()
    obj_view = view(root)
    root.mainloop()


class view:
    global all_names
    global all_ids
    global students

    def __init__(self, root):
        # ----------- gui coding of application ------------------
        root.geometry("560x400")
        root.title("Automatic Student's Attendance System")
        root.configure(background="#fff")
        self.root = root

        self.lb_headding = ttk.Label(
            self.root, text="Welcome to Automatic Student's Attendance System ! ",font="Ariel 15 italic",background="#fff")
        self.lb_headding.configure(borderwidth=5,relief="raised")
        self.lb_headding.grid(row=0,column=0, columnspan=4)

        self.selection = tk.IntVar()
        self.rb_tracking = ttk.Radiobutton(
            self.root, text="Start Tracking", command=self.rb_option_select, variable=self.selection, value=1)
        self.rb_tracking.grid(row=1,column=0,columnspan=4,sticky=tk.W,pady=5,padx=5)

        self.rb_Insert_Data = ttk.Radiobutton(
            self.root, text="Insert Student's data", command=self.rb_option_select, variable=self.selection, value=2)
        self.rb_Insert_Data.grid(row=2,column=0,columnspan=4,pady=5,padx=5,sticky=tk.W)

        self.btn_proceed = ttk.Button(self.root, text="Proceed")
        self.btn_proceed.bind("<Button>", self.rb_option_select)
        self.btn_proceed.grid(row=3,column=1,columnspan=2)
        # self.lb_headding.pack()
        #self.rb_tracking.pack()
        #self.rb_Insert_Data.pack()
        #self.btn_proceed.pack()

        # ------------------------------------------------------
        self.obj_controller = controller.controller()

    def rb_option_select(self, e=0):

        self.option = self.selection.get()

        if self.option == 1:  # "start tracking" selected
            self.btn_proceed.bind("<Button>", self.Start_tracking)

        elif self.option == 2:  # "insert data" selected
            self.btn_proceed.bind("<Button>", self.Start_insert_data)

        else:  # if no option selected,then, self.options == 0
            print("no option given ", self.option)
            messagebox.showinfo("NO SELECTION!", "Plese select an option.")

    def Start_tracking(self, e):

        print("tracking")
        self.obj_controller.face_recognizer()

    def Start_insert_data(self, e):
        print("inserting data")

        # if (name and sid):  # if both name and sid is given

        self.window2 = tk.Tk()
        self.window2.geometry("687x526+558+155")
        self.window2.title(" ENTER STUDENT'S DATA ")
        self.window2.configure(background="#fff")

        self.lb_head = ttk.Label(
            self.window2, text="Enter the student's details.")
        self.lb_name = ttk.Label(self.window2, text="Student's Name :")
        self.lb_id = ttk.Label(self.window2, text="Student's ID :")

        self.ent_name = ttk.Entry(self.window2)
        self.ent_id = ttk.Entry(self.window2)

        self.btn_store = ttk.Button(self.window2, text="Store info")
        # when "store" butten is pressed
        self.btn_store.bind("<Button>", self.Store_data)

        self.btn_train = ttk.Button(self.window2, text="Train model")
        # when "train" butten is pressed
        self.btn_train.bind("<Button>", self.trainer)

        self.lb_head.grid(row=0, column=0)
        self.lb_name.grid(row=1, column=0)
        self.lb_id.grid(row=2, column=0)
        self.ent_name.grid(row=1, column=1)
        self.ent_id.grid(row=2, column=1)
        self.btn_store.grid(row=3, column=0)
        self.btn_train.grid(row=3, column=1)

        self.window2.mainloop()

    def Store_data(self, e):  # when "store" butten is pressed

        print("img capture")

        s_name = self.ent_name.get()
        s_id = self.ent_id.get()

        print("name :", s_name, "        id:", s_id)
        print(self.obj_controller.obj_model.all_ids)

        if (s_id and s_name):  # when both name and id is given
            s_id = int(s_id)
            if (s_id not in self.obj_controller.obj_model.all_ids):  # given id is unique (i.e. not already present)

                #adding new student's data
                self.obj_controller.trainingOngoing = True
                self.obj_controller.Video_capture(s_id, s_name)
                self.obj_controller.sample_count = 0
                self.obj_controller.trainingOngoing = False

                #updating lists
                status = self.obj_controller.insert_record(s_name,s_id)  
                messagebox.showinfo("Info", "Data successfully inserted!")

            else:  # if given id is already present
                messagebox.showinfo(
                    "Info", "A student with id " + str(s_id) + " already present!")

        elif not(s_id) or not(s_name):  # if any one of them (name or id ) is not entered
            messagebox.showinfo("COMPLETE DATA NOT GIVEN!",
                                "Plese insert all values!")

    def trainer(self, e):  # when "train" butten is pressed

        print("tarining the model")
        result = self.obj_controller.trainer()
        if result == True:
            messagebox.showinfo("Model Trainer Info",
                                "Model is trained successfully!")
        else:
            messagebox.showinfo("Something went wrong :-(",
                                "Sorry, unable to train the model.")


if __name__ == '__main__':

    start_gui()
