# sleep-tracker
Simple GUI that calculates what time you should sleep and keeps track of your sleep everyday with a CSV file 
(not completely finished)

![image](ss1.PNG)

![image](ss2.PNG)

## Calculator Page 
* Enter the length of preferred sleep cycle (in minutes) and enter what time you want to wake up and whether AM or PM 
* Click generate to view what times you should sleep 
* If you do not have to wake up a certain time, leave Target Time blank and the script will calculate what time you should wake up given you sleep then.  
* Click Graph to view the graphing page 

## Graph Page
* Choose whether you want a day, week, or month bin size and choose which plot you want to see 
* Hit clear plot after cuz I haven't figured out how to clear it after every plot click yet
* Click Calculator to go back to calculator page

## What I used
* Tkinter for GUI
* Matplotlib for graphs
* Pandas to work with the csv file 
* Datetime to work with time stuff
