from tkinter import *
import datetime as datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


class main(Tk): # https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        container = Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (calculatorPage, graphPage):
            frame = F(container, self)
            
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.show_frame(calculatorPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class graphPage(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        # controller.geometry('1000x1000')

        self.days_of_week = {'0': 'MON', '1': 'TUE', '2' : 'WED', '3': 'THU', '4' : 'FRI', '5' : 'SAT', '6' : 'SUN'}

        self.calculator_button = Button(self, text = "Calculator", command = lambda : controller.show_frame(calculatorPage))
        self.calculator_button.grid(row = 3, column = 2, padx = 5, pady = 5)
        
        self.scatter_button = Button(self, text = "Bar Plot", command = self.bar_plot)
        self.scatter_button.grid(row = 0, column = 2, padx = 5, pady = 5)

        self.line_button = Button(self, text = "Line Plot", command = self.line_plot)
        self.line_button.grid(row = 1, column = 2, padx = 5, pady = 5)

        self.clear_button = Button(self, text = "Clear Plot", command = self.clear_plot)
        self.clear_button.grid(row = 2, column = 2, padx = 5, pady = 5)

        self.bin = StringVar()
        self.bin.set("Day")
        self.bin_entry = OptionMenu(self, self.bin, *["Day", "Week", "Month"])
        self.bin_entry.grid(row = 0, column = 3)

        self.fig = Figure(figsize = (8, 5), dpi = 150)
        self.plot = self.fig.add_subplot(111)
        self.plot.set_xlabel("Date", size = 6)
        self.plot.set_ylabel("Cycles", size = 6)
        self.plot.tick_params(axis = 'x', labelsize = 4, rotation = 30)
        self.canvas = FigureCanvasTkAgg(self.fig, master = self)
        self.canvas.get_tk_widget().grid(row = 0, column = 0)

        self.times = calculatorPage.create_file(self)
        self.times['Date'] = pd.to_datetime(self.times['Date']) # 1 (optim.)

        self.toolbarFrame = Frame(master=self) # https://stackoverflow.com/questions/12913854/displaying-matplotlib-navigation-toolbar-in-tkinter-via-grid (LBoss)
        self.toolbarFrame.grid(row= 1,column=0)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

    def bar_plot(self): 
        option = self.bin.get()
        if option == "Week":
            df = self.group_week()
            self.plot.set_xticks(df['Date']) # https://stackoverflow.com/questions/3486121/how-to-plot-data-against-specific-dates-on-the-x-axis-using-matplotlib
            self.plot.set_xticklabels([date.strftime('%m-%d-%Y') for date in df['Date']])
            self.plot.bar(df['Date'], df['Cycles'])
        self.canvas.draw()
    
    def line_plot(self):
        option = self.bin.get()
        if option == "Week": 
            df = self.group_week()
            self.plot.set_xticks(df['Date'])
            self.plot.set_xticklabels([date.strftime('%m-%d-%Y') for date in df['Date']])
            self.plot.plot(df['Date'], df['Cycles'])
        self.canvas.draw()

    def clear_plot(self):
        self.plot.cla()
        self.plot.set_xlabel("Date", size = 6)
        self.plot.set_ylabel("Cycles", size = 6)
        self.plot.tick_params(axis = 'x', labelsize = 4, rotation = 30)
        self.canvas.draw()
    
    def group_week(self): 
        first_day = self.times.iloc[0]['Date']
        freq = 'W-' + self.days_of_week[str(first_day.weekday())]
        return self.times.groupby(pd.Grouper(key='Date', freq=freq))['Cycles'].sum().reset_index() #https://stackoverflow.com/questions/45281297/group-by-week-in-pandas/45281439


class calculatorPage(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self.times = self.create_file()

        self.cycle_label = Label(self, text = "Cycle Length", font = ('bold', 12))
        self.cycle_label.grid(row=0, column=0, pady = 20)
        self.cycle_entry = Entry(self)
        self.cycle_entry.grid(row = 0, column = 1)

        self.target_label = Label(self, text = "Target Time", font = ('bold', 12))
        self.target_label.grid(row = 0, column = 2, pady = 20)
        self.target_entry = Entry(self)
        self.target_entry.grid(row = 0, column = 3)

        self.time_text = StringVar()
        self.time_text.set("AM")
        self.time_entry = OptionMenu(self, self.time_text, *["AM", "PM"])
        self.time_entry.grid(row = 0, column = 4)

        self.time_list = Listbox(self, height = 6, width = 18, font = ('Times', 14))
        self.time_list.grid(row = 3, column = 1, columnspan = 3, rowspan = 7, pady= 5, padx= 9)

        self.generate_button = Button(self, text = "generate", font = ('bold', 12), width = 10, command = self.generate_time)
        self.generate_button.grid(row = 2, column = 2)

        self.transfer_button = Button(self, text = "transfer", font = ('bold', 12), width = 10, command = self.input_time)
        self.transfer_button.grid(row = 10, column = 2)

        self.graph_button = Button(self, text = "Graph", command = lambda : controller.show_frame(graphPage))
        self.graph_button.grid(row = 3, column = 3, padx = 5, pady = 5)

     
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

    def create_file(self): # check if csv file in directory
        try:
            times = pd.read_csv('times.csv', index_col=[0])
            return times
        except:
            times = pd.DataFrame(columns=['Date', "Sleep Time", "Wake Time", "Cycles", "Cycle Length"])
            times.to_csv('times.csv')
            times = pd.read_csv('times.csv', index_col=[0])
            return times




if __name__ == "__main__":
    app = main()
    app.mainloop()
