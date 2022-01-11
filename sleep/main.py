from tkinter import *

import datetime as datetime

import pandas as pd

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)


# https://www.pythoncharts.com/matplotlib/beautiful-bar-charts-matplotlib/

class main(Tk): # https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
    # class that controls which frames are displayed 

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
        frame.reset()
        frame.tkraise()


class graphPage(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        
        self.controller = controller
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
        self.times['Date'] = pd.to_datetime(self.times['Date']) # 1 (optimize)

        self.toolbarFrame = Frame(master=self) # https://stackoverflow.com/questions/12913854/displaying-matplotlib-navigation-toolbar-in-tkinter-via-grid (LBoss)
        self.toolbarFrame.grid(row= 1,column=0)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbarFrame)

    def bar_plot(self):
        df = self.times
        option = self.bin.get()
        if option == 'Day':
            df = self.group_day()
        elif option == "Week":
            df = self.group_week()
        else:
            df = self.group_month()
            # self.plot.set_xticks(df['Date']) ERROR: (matplotlib.units.ConversionError: Failed to convert value(s) to axis units)
            # self.plot.set_xticklabels(df['Date'])
            self.plot.bar(df['Date'], df['Cycles'])
            self.plot.set_axisbelow(True)
            self.plot.yaxis.grid(True, color = '#EEEEEE')
            self.canvas.draw()
            return
        self.plot.set_xticks(df['Date']) # https://stackoverflow.com/questions/3486121/how-to-plot-data-against-specific-dates-on-the-x-axis-using-matplotlib
        self.plot.set_xticklabels([date.strftime('%m-%d-%Y') for date in df['Date']])
        self.plot.bar(df['Date'], df['Cycles'])
        self.plot.set_axisbelow(True)
        self.plot.yaxis.grid(True, color = '#EEEEEE')
        self.canvas.draw()
    
    def line_plot(self):
        df = self.times
        option = self.bin.get()
        if option == 'Day':
            df = self.group_day()
        elif option == "Week":
            df = self.group_week()
        else:
            df = self.group_month()
            self.plot.plot(df['Date'], df['Cycles'], marker = ".", markersize = 5, linewidth = 1.3)
            self.plot.set_axisbelow(True)
            self.plot.yaxis.grid(True, color = '#EEEEEE')
            self.canvas.draw()
            return
        self.plot.set_xticks(df['Date'])
        self.plot.set_xticklabels([date.strftime('%m-%d-%Y') for date in df['Date']])
        self.plot.plot(df['Date'], df['Cycles'], marker = ".", markersize = 5, linewidth = 1.3)
        self.plot.set_axisbelow(True)
        self.plot.yaxis.grid(True, color = '#EEEEEE')
        self.plot.fill_between(df['Date'], 0, df['Cycles'], alpha = .5)
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

    def group_month(self):
        return self.times.groupby(self.times['Date'].dt.strftime('%b-%Y'))['Cycles'].sum().reset_index().sort_values('Date', ascending= False)

    def group_day(self):
        return self.times.groupby(pd.Grouper(key='Date', freq='D'))['Cycles'].sum().reset_index() 

    def reset(self):
        self.controller.geometry('1350x875')

class calculatorPage(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)

        self.controller = controller
        self.controller.title('Sleep Calculator')
        self.times = self.create_file()

        self.cycle_label = Label(self, text = "Cycle Length", font = ('bold', 12))
        self.cycle_label.grid(row=0, column=0, pady = 20)
        self.cycle_entry = Entry(self)
        self.cycle_entry.grid(row = 0, column = 1)

        self.target_label = Label(self, text = "Target Time", font = ('bold', 12))
        self.target_label.grid(row = 0, column = 2, pady = 20)
        self.target_entry = Entry(self)
        self.target_entry.grid(row = 0, column = 3)

        self.am_pm = StringVar()
        self.am_pm.set("AM")
        self.ampm_entry = OptionMenu(self, self.am_pm, *["AM", "PM"])
        self.ampm_entry.grid(row = 0, column = 4)

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
        cycle_mins = datetime.timedelta(minutes = int(self.cycle_entry.get()))
        target_time = self.target_entry.get()
        if target_time == "":
            now = datetime.datetime.now()
            for i in range(1, 7):
                now += cycle_mins
                self.time_list.insert(i, str(i) + " cycle(s) - " + now.strftime(format))
        else:
            period = self.am_pm.get()
            target_time = self.target_entry.get() + " " + period
            target_time = datetime.datetime.strptime(target_time, format)
            # delta = datetime.timedelta(hours = t.hour, minutes = t.minute)
            for i in range(1, 7):
                target_time -= cycle_mins
                self.time_list.insert(i, str(i) + " cycle(s) - " + target_time.strftime(format))
    
    def extract_time(self): # return data you inputted into input_time()
        time = self.time_list.get(self.time_list.curselection())
        sleep_time = datetime.datetime.now().strftime("%I:%M %p")
        if self.target_entry.get() == "":
            return sleep_time, time[-8::],  time[0]
        return time[-8::], self.target_entry.get(), time[0] # return format: [sleep time, wake up time, # of cycles]
    
    def input_time(self): # input data into dataframe (input sleep date day before wake day)
        sleep_time, wake_time, cycles = self.extract_time()
        today = datetime.datetime.now()
        if today.strftime('%p') == 'AM':
            today -= datetime.timedelta(days = 1)
        today = today.strftime("%m/%d/%Y")
        self.times = self.times.append({'Date' : today, 'Sleep Time': sleep_time, "Wake Time": wake_time + ' ' + self.am_pm.get(), "Cycles": cycles, "Cycle Length": self.cycle_entry.get()}, ignore_index = True)
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
    
    def reset(self):
        self.controller.geometry('550x400')


if __name__ == "__main__":
    app = main()
    app.mainloop()
