# App name : Activity Tracker
# Created by: Ashwani Bhati
# Created this to track my daily activities. 
# Yes, there are other applications to track daily activities and if not there is good old EXCEL file & Macro to do all this. 
# But I would not have learned about Classes, Tkinter etc if not for this app.
# This is simple app that takes input as activity name and starts the timer, user can stop the timer and the data is logged in an excel file.
# Excel file is displayed using Treeview in the app.
# I learned building this from corey schafer & codemy.com & a little bit of Chatgpt for doubts.



#imported libraries
from tkinter import PhotoImage
import tkinter as tk
from tkinter import ttk
import pandas as pd
import openpyxl
from datetime import datetime,timedelta

#main function
def main():
    app = Application()
    app.mainloop()

            
#ExcelFile class to load excel
# If excel file is not present then create a new one with headers.            
class ExcelFile():
    def __init__(self):
        self.excel_file_name = "F:\\Python\\activity_tracker_excel.xlsx"
        try:
            self.excel_data = self.excel_read()
            self.workbook = openpyxl.load_workbook(self.excel_file_name)
            self.sheet = self.workbook.active
            self.headers = self.excel_data.columns.to_list()
        except:
            print(f'ERROR : No Excel file found. Creating a new one with name {self.excel_file_name} .')
            self.initialize_excel(self.excel_file_name)    
        self.row = []
        
    #this initialize a new excel file        
    def initialize_excel(self,excel_file_name):
        # Create a new workbook and select the active worksheet
        self.workbook = openpyxl.Workbook()
        self.sheet = self.workbook.active
        
        # Set the header row
        self.headers = ['date',	'activity',	'start_time', 'stop_time', 'duration']

        self.sheet.append(self.headers)
        
        # Save the workbook
        self.workbook.save(excel_file_name)

    # read exisitng excel file for printing in treeview 
    #should show today's data only
    def excel_read(self):
        df1 = pd.read_excel(self.excel_file_name)
        df1['date'] = pd.to_datetime(df1['date']).dt.date
        df2 = df1[df1['date']==datetime.date(datetime.now())]
        return df2
    
    #write activity log in the excel file
    def write_excel(self,row):            
        self.sheet.append(row)
        self.workbook.save(self.excel_file_name)
        print(f"Row saved: {row}")

    #create start row based on activity start and there will be no end time.
    def create_start_row(self,date,activity,start_time):
        self.row = [date,activity,start_time]
        #print(self.row)

    #creates entire row with data once the activity stops    
    def create_stop_row(self,stop_time):
        duration = stop_time - self.row[2]
        self.row.append(stop_time)
        self.row.append( duration)
        self.write_excel(self.row)
        #print(self.row) 

#Class application for tkiner
# loads image for icon
# creating 3 frames: 1. Input and showing what was the input, 2. For treeview of excel file, 3. for timer, start, stop button.
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Activity Tracker by Ashwani")
        p1 = PhotoImage(file = "F:\\Ashwani\\Ashwani Social Media Content\\Logo\\TheHorsesKing_Linkedin1.png") 
        self.iconphoto(False,p1)
        self.geometry("1200x400")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.excel_instance = ExcelFile()

        self.frame1 = InputForm(self,self.excel_instance)
        self.frame1.grid(row=0,column=0,sticky="nsew",padx=5,pady=5)    

        self.frame2 = Timer(self,self.excel_instance)
        self.frame2.grid(row=0,column=1,sticky="nsew",padx=5,pady=5)    

        self.frame3 = TreeView(self,self.excel_instance)
        self.frame3.grid(row=1,column=0,sticky="nsew",padx=5,pady=5)    

#treeview for showing excel file as logs
class TreeView(ttk.Frame):

    def __init__(self, parent,excel_instance):
        super().__init__(parent)
        self.parent = parent  # Store reference to Application
        self.excel_instance = excel_instance  
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.my_tree = ttk.Treeview(self)

    #defines treeview for excel
    def tree_view(self):
            #clear treeview
            self.my_tree.delete(*self.my_tree.get_children())
            df= self.excel_instance.excel_read()  
                #setup new treeview
            self.my_tree['column']  = list(df.columns)
            self.my_tree['show'] = 'headings'

            #loop throught column list
            for column in self.my_tree['column']:
                self.my_tree.heading(column, text=column)

            #put data in treeview
            df_rows = df.to_numpy().tolist()      

            for row in df_rows:
                self.my_tree.insert('','end',values=row)
            
            self.my_tree.pack()

#class InputForm takes all the input and displays it
class InputForm(ttk.Frame):

    def __init__(self, parent,excel_instance):
        super().__init__(parent)
        self.parent = parent  # Store reference to Application
        self.excel_instance = excel_instance  
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.entry = ttk.Entry(self)
        self.entry.grid(row=0,column=0,sticky='ew')
        
        self.entry.bind("<Return>",self.add_to_list)

        front_text = "Welcome to The Activity Tracker.\nDesigned and developed by Ashwani Bhati in Sweden."

        self.my_label = tk.Label(self,width=700,bg="white",text=front_text,borderwidth=0,font=("Calibri",20))
        self.my_label.grid(row=1,column=0,columnspan=3,sticky="nsew")
    
    #this adds data to list and displays label of current activity. Once some data is entered in box, it will start timer as well.
    # deletes the entered text after storing in text variable
    # set the time and activity name
    # prints label with activity data
    def add_to_list(self,_event=None):
        text = self.entry.get()
        if text and self.master.frame2.text == '00:00:00' :
            #starts the timer once entry is given
            self.master.frame2.start()
            #delete the given input or clear input field
            self.entry.delete(0,tk.END)
            #notes the start time and activity name
            self.activty_date = datetime.date(datetime.now())
            self.activity_name = text
            self.start_time = datetime.now().replace(microsecond=0)
            #updating excel file for start data
            self.excel_instance.create_start_row(self.activty_date, self.activity_name, self.start_time)  
            #display label with row data
            self.print_label('started',self.start_time)
            #display excel in treeview at the start of activity.
            self.master.frame3.tree_view() 
    
    #printing activity data in the label
    def print_label(self,status,time):
        if status == 'started':
            label_text = f'{self.activity_name} {status} at {time}.' 
        else:
            label_text = f'{self.activity_name} {status} at {time}.\nDuration : {time-self.start_time}' 
        self.my_label.config(text=label_text)            
            

#class Timer is for running the timer and using start/ stop functioning    
class Timer(ttk.Frame):
    def __init__(self, parent,excel_instance):
        super().__init__(parent)
        self.excel_instance = excel_instance
        self.seconds  = 0
        self.minutes  = 0
        self.hours    = 0
        self.text     = "%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds )
        self.carry_on = True
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
       
        self.ScoreL = ttk.Label(self, text = self.text,width=10,borderwidth=0,font=("Calibri",20))
        self.ScoreL.grid(row=0, column=0, sticky='NSWE')

        self.start_btn = ttk.Button(self, text="START", command = self.start_add_to_list)
        self.start_btn.grid(row=2, column=0, sticky='NSWE')

        self.stop_btn = ttk.Button(self, text="STOP", command =self.stop)
        self.stop_btn.grid(row=1, column=0, sticky='NSWE')
    
    #this updates the timer
    def update(self):
        if self.carry_on == True:
            self.seconds += 1
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
            if self.minutes == 60:
                self.minutes = 0
                self.hours += 1
            self.text = "%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds )
            self.ScoreL.configure(text=self.text)
            if self.carry_on == True:
                # schedule next update 1 second later
                self.master.after(1000, self.update)
    
    #this resetes the timer
    def reset_time(self):
        self.seconds  = 0   
        self.minutes  = 0
        self.hours    = 0
        self.text = "%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds )
        self.ScoreL.configure(text=self.text)

    #this starts the timer by not allowing timer to start if it is already running
    def start(self):
        if self.text == '00:00:00':
            self.reset_time()
            self.carry_on = True
            self.master.after(1000, self.update)

    #this stops the timer and only works when timer is running
    #this notes the end time of activity
    def stop(self):
        if self.text != '00:00:00':
            self.carry_on = False        
            print(f'Stopped at : {self.text}')
            self.stop_time = datetime.now().replace(microsecond=0)
            #creating complete row for activity data once activity stops.
            self.excel_instance.create_stop_row(self.stop_time)  
            #resetting time once activity is completed.
            self.reset_time()     
            #reloads tree view once activity is done to display last activity    
            self.master.frame3.tree_view() 
            #print label with activity data
            self.master.frame1.print_label('stopped',self.stop_time)  # activity completion        

    #this action is taken when stop button is pressed.
    def start_add_to_list(self):
        self.master.frame1.add_to_list()  # Use existing instance
        self.master.frame3.tree_view()
            
if __name__ =='__main__':
    main()