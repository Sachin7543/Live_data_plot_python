import serial # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
import matplotlib.pyplot as plt2
from drawnow import *
import time

Obj= []
Die=[]
arduinoData = serial.Serial('COM4', 9600) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0
size = 10
i = 0
averages = []

def makeFig(): #Create a function that makes our desired plot
    timestr = time.strftime("%d/%m/%Y-%H:%M:%S")
    plt.ylim(20,50)                                 #Set y min and max values
    plt.title('Live Streaming Sensor Data\n'+timestr)      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('Temp')                            #Set ylabels
    plt.plot(averages)       #plot the temperature
    plt2.plot(Die) #plot Die data
    plt2.xlabel('Sensor Data range')                    #label second y axis
    plt2.ticklabel_format(useOffset=False)           #Force matplotlib to NOT autoscale y axis
    plt.legend(["Obj Tempture","Die Temperture"])                  #plot the legend
    
while True: # While loop that loops forever
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.readline() #read the line of text from the serial port
    strR=arduinoString.decode()
    arduinoString= strR.rstrip()
    dataArray = arduinoString.split(',')   #Split it into an array called dataArray
    if ( len(dataArray)==2):
        if (len(dataArray[0])== 5):
            temp = float( dataArray[0])            #Convert first element to floating number and put in temp
            Obj.append(temp)
            if (len(Obj) > size):
                value = Obj[i : i + size]
                average = sum(value) / size
                averages.append(average)
                i += 1
                 #averages.append(temp)
        if (len(dataArray[1])== 5):
            P =    float( dataArray[1])            #Convert second element to floating number and put in P
            Die.append(P)
    drawnow(makeFig)                       #Call drawnow to update our live graph
    plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
    cnt=cnt+1
    if(cnt>1000):                            #If you have 50 or more points, delete the first one from the array
        Obj.pop(0)                       #This allows us to just see the last 50 data points
        Die.pop(0)
