import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamOutlet, StreamInfo

class FFT:
    def __init__(self, x = [], y = []) -> None:
        self.x = x # timestamp
        self.y = y # amplitude
        self.info = StreamInfo("backendMarker", "Markers", 1, 0, channel_format="string") # Initialize the info for the output marker Stream that we will be sending to Godot and possibly drone controller
        self.outlet = StreamOutlet(self.info) # initialize the outlet Stream
        self.currMovement = ""
        self.currScreen = "main" #other screens include view, movement, and rotation

    def setTimestamps(self,x):
        self.x = x

    def setAmplitude(self,y):
        self.y = y

    def addTimestamp(self,x):
        self.x.append(x)

    def addAmplitude(self,y):
        self.y.append(y)
    
    def transform(self):
        # This method does the actual FFT and will plot the FFT Plot
        # x-axis is frequency, y-axis is magnitude
        output = np.fft.fft(self.y)
        freqs = np.abs(np.fft.fftfreq(len(self.y), d=self.x[1] - self.x[0])) # Need clarification on this
        magnitude = np.abs(output)
        highest = -1
        index = -1
        for i in range(len(magnitude)):
            if magnitude[i] > highest and freqs[i] > 1:
                highest = magnitude[i]
                index = i
        #self.outlet.push_sample([freqs[index]])
        print("The Frequency is:", freqs[index])
        #print(type(freqs[index]))

        temp = self.currMovement
        if self.currScreen == "main":
            if 30.5 <= float(freqs[index]) < 31.5:
                temp = "moveDown"
            elif 29.5 <= float(freqs[index]) < 30.5:
                temp = "moveForward"
            elif 28.5 <= float(freqs[index]) < 29.5:
                temp = "moveBackward"
        elif self.currScreen == "movement":
            if 30.5 <= float(freqs[index]) < 31.5:
                temp = "moveDown"
            elif 29.5 <= float(freqs[index]) < 30.5:
                temp = "moveForward"
            elif 28.5 <= float(freqs[index]) < 29.5:
                temp = "moveBackward"
        elif self.currScreen == "rotation":
            if 30.5 <= float(freqs[index]) < 31.5:
                temp = "moveDown"
            elif 29.5 <= float(freqs[index]) < 30.5:
                temp = "moveForward"
            elif 28.5 <= float(freqs[index]) < 29.5:
                temp = "moveBackward"
        elif self.currScreen == "view":
            if 30.5 <= float(freqs[index]) < 31.5:
                temp = "moveDown"
            elif 29.5 <= float(freqs[index]) < 30.5:
                temp = "moveForward"
            elif 28.5 <= float(freqs[index]) < 29.5:
                temp = "moveBackward"

        self.currMovement = temp
        self.outlet.push_sample([temp]) 
        #plt.plot(freqs,magnitude)
        #plt.show()


    def plotRaw(self):
        # This doesn't do anything besides plot the input, x-axis is time, y-axis is amplitude
        plt.plot(self.x,self.y)
        plt.show()
