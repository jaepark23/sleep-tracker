from tkinter import *
import datetime as datetime
import pandas as pd


# if sleep time has passed dont display it 
# create sleep graphs


class calculatorPage():
    def __init__(self, master):
        self.times = self.create_file()

        self.master = master
        master.title("Sleep Calculator")
        master.geometry("550x300")
    
        # self.cycle_text = StringVar()
        self.cycle_label = Label(master, text = "Cycle Length", font = ('bold', 12), pady = 20)
        self.cycle_label.grid(row=0, column=0)
        self.cycle_entry = Entry(master)
        self.cycle_entry.grid(row = 0, column = 1)

        # self.target_text = StringVar()
        self.target_label = Label(master, text = "Target Time", font = ('bold', 12), pady = 20)
        self.target_label.grid(row = 0, column = 2)
        self.target_entry = Entry(master)
        self.target_entry.grid(row = 0, column = 3)

        self.time_text = StringVar()
        self.time_text.set("AM")
        self.time_entry = OptionMenu(master, self.time_text, *["AM", "PM"])
        self.time_entry.grid(row = 0, column = 4)

        self.time_list = Listbox(master, height = 6, width = 18, font = ('Times', 14))
        self.time_list.grid(row = 3, column = 1, columnspan = 3, rowspan = 7, pady= 5, padx= 9)

        self.generate_button = Button(master, text = "generate", font = ('bold', 12), width = 10, command = self.generate_time)
        self.generate_button.grid(row = 2, column = 2)

        self.transfer_button = Button(master, text = "transfer", font = ('bold', 12), width = 10, command = self.input_time)
        self.transfer_button.grid(row = 10, column = 2)

    def create_file(self): # check if csv file in directory
        try:
            df = pd.read_csv('times.csv', index_col=[0])
        except:
            df = pd.DataFrame(columns=['Date', "Sleep Time", "Wake Time", "Cycles", "Cycle Length"])
            df.to_csv('times.csv')
            df = pd.read_csv('times.csv', index_col=[0])
        return df   
     
    def generate_time(self): # generate list of sleep times 
        self.time_list.delete(0, 'end')
        format = "%I:%M %p"
        c = datetime.timedelta(minutes = int(self.cycle_entry.get()))
        wake_time = self.target_entry.get()
        if wake_time == "":
            n = datetime.datetime.now()
            for i in range(1, 7):
                n += c
                self.time_list.insert(i, str(i) + " cycle(s) - " + n.strftime(format))
        else:
            period = self.time_text.get()
            wake_time = self.target_entry.get() + " " + period
            t = datetime.datetime.strptime(wake_time, format)
            # delta = datetime.timedelta(hours = t.hour, minutes = t.minute)
            for i in range(1, 7):
                t -= c
                self.time_list.insert(i, str(i) + " cycle(s) - " + t.strftime(format))
    
    def extract_time(self): # return data you inputted into input_time()
        time = self.time_list.get(self.time_list.curselection())
        sleep_time = datetime.datetime.now().strftime("%I:%M %p")
        if self.target_entry.get() == "":
            return sleep_time, time[-8::],  time[0]
        return time[-8::], self.target_entry.get(), time[0] # return format: [what time sleep, wake up time, # of cycles]
    
    def input_time(self): # input data into dataframe 
        sleep_time, wake_time, cycles = self.extract_time()
        today = datetime.datetime.now()
        today = today.strftime("%m/%d/%Y")
        self.times = self.times.append({'Date' : today, 'Sleep Time': sleep_time, "Wake Time": wake_time + ' ' + self.time_text.get(), "Cycles": cycles, "Cycle Length": self.cycle_entry.get()}, ignore_index = True)
        self.times.to_csv('times.csv')

root = Tk()

gui = calculatorPage(root)

root.mainloop()

