import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamOutlet, StreamInfo
from ssvep import ssvep





class FFT:
    def __init__(self, x = [], y = []) -> None:
        self.x = x # timestamp
        self.y = y # amplitude
        self.info = StreamInfo("backendMarker", "Markers", 1, 0, channel_format="string") # Initialize the info for the output marker Stream that we will be sending to Godot and possibly drone controller
        self.outlet = StreamOutlet(self.info) # initialize the outlet Stream
        self.curMovement = ""
        self.curScreen = "main" #other screens include view, movement, and rotation


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
        fft = np.fft.fft(self.y, axis=0)
        mean_power = np.mean((np.abs(fft)**2), axis=1)
        freqs = np.fft.fftfreq(len(self.y), 1/200)
        freq,_ = ssvep(mean_power,freqs)

        print("The Frequency is:", freq)
        #print(type(freqs[index]))
        self.curMovement = "None"
        if self.curScreen == "main":
            if 4 <= float(freq) < 6.5: #! 13 Hz (NEEDS TO BE CHANGED EVENTUALLY)
                self.curMovement = "movement"
                self.curScreen = "movement"
            elif 6.5 <= float(freq) < 9: # 15 Hz
                self.curMovement = "view"
                self.curScreen = "view"
            elif 9 <= float(freq) < 12.5: # 11 Hz
                self.curMovement = "rotation"
                self.curScreen = "rotation"
        elif self.curScreen == "movement":
            if 8.5 <= float(freq) < 9.5: # 9 Hz
                self.curMovement = "moveUp"
            elif 10.5 <= float(freq) < 11.5: # 11 Hz
                self.curMovement = "moveDown"
            elif 29.5 <= float(freq) < 30.5: #! 13 Hz (NEEDS TO BE CHANGED EVENTUALLY)
                self.curMovement = "moveForward"
            elif 7.5 <= float(freq) < 8.5: # 8 Hz
                self.curMovement = "moveBackward"
            elif 13.5 <= float(freq) < 14.5: # 14 Hz
                self.curMovement = "moveRight"
            elif 14.5 <= float(freq) < 15.5: # 15 Hz
                self.curMovement = "moveLeft"
        elif self.curScreen == "rotation":
            if 8.5 <= float(freq) < 9.5:
                self.curMovement = "bankUp"
            elif 10.5 <= float(freq) < 11.5:
                self.curMovement = "bankDown"
            elif 12.5 <= float(freq) < 13.5:
                self.curMovement = "rotateRight"
            elif 14.5 <= float(freq) < 15.5:
                self.curMovement = "rotateLeft"
        elif self.curScreen == "view":
            if 11.5 <= float(freq) < 12.5:
                self.curMovement = "goBack"
        print(self.curMovement)
        self.outlet.push_sample([self.curMovement]) 


    def plotRaw(self):
        # This doesn't do anything besides plot the input, x-axis is time, y-axis is amplitude
        plt.plot(self.x,self.y)
        plt.show()
