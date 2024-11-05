import numpy as np
import matplotlib.pyplot as plt
from pylsl import StreamOutlet, StreamInfo

class FFT:
    def __init__(self, freq_map = {}, x = [], y = []) -> None:
        self.x = x # timestamp
        self.y = y # amplitude
        self.info = StreamInfo("backendMarker", "Markers", 1, 0, channel_format="string") # Initialize the info for the output marker Stream that we will be sending to Godot and possibly drone controller
        self.outlet = StreamOutlet(self.info) # initialize the outlet Stream
        self.currMovement = ""
        self.currScreen = "main" #other screens include view, movement, and rotation
        self.freq_map = freq_map

    def setTimestamps(self,x):
        self.x = x

    def setAmplitude(self,y):
        self.y = y

    def addTimestamp(self,x):
        self.x.append(x)

    def addAmplitude(self,y):
        self.y.append(y)
    
    def compute_FFT(self):
        # This method does the actual FFT and will plot the FFT Plot
        # x-axis is frequency, y-axis is magnitude
        channels = [list(col) for col in zip(*self.y)]
        freqs_per_channel = []
        for i in channels:
            output = np.fft.fft(i)
            freqs = np.abs(np.fft.fftfreq(len(i), d=self.x[1] - self.x[0])) # Need clarification on this
            magnitude = np.abs(output)
            highest = -1
            index = -1
            for i in range(len(magnitude)):
                if magnitude[i] > highest and freqs[i] > 1:
                    highest = magnitude[i]
                    index = i
            #self.outlet.push_sample([freqs[index]])
            print("The Frequency is:", freqs[index])
            freqs_per_channel.append(freqs[index])
            plt.figure(figsize=(10, 5))
            plt.plot(freqs[:len(freqs)//2], magnitude[:len(magnitude)//2])  # Only positive frequencies
            plt.title(f'FFT Spectrum for Channel {i + 1}')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')
            plt.show()
        avg_freq = sum(freqs_per_channel)/len(freqs_per_channel)
        return(avg_freq)

    def outputControl(self):
        input = round(self.compute_FFT())
        #use this freqenciy and map it to the control then return that control (should be a string return)
        
        


    def transform(self):
        # This method does the actual FFT and will plot the FFT Plot
        # x-axis is frequency, y-axis is magnitude
        channels = [list(col) for col in zip(*self.y)]
        freqs_per_channel = []
        for i in channels:
            output = np.fft.fft(i)
            freqs = np.abs(np.fft.fftfreq(len(i), d=self.x[1] - self.x[0])) # Need clarification on this
            magnitude = np.abs(output)
            highest = -1
            index = -1
            for i in range(len(magnitude)):
                if magnitude[i] > highest and freqs[i] > 1:
                    highest = magnitude[i]
                    index = i
            #self.outlet.push_sample([freqs[index]])
            print("The Frequency is:", freqs[index])
            freqs_per_channel.append(freqs[index])
        avg_freq = sum(freqs_per_channel)/len(freqs_per_channel)
        print(avg_freq)
        '''
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
        '''
        freqs = [100] #temporary
        index = 0 #temporary

        temp = self.currMovement
        if self.currScreen == "main":
            if 29.5 <= float(freqs[index]) < 30.5: #! 13 Hz (NEEDS TO BE CHANGED EVENTUALLY)
                temp = "movement"
                self.currScreen = "movement"
            elif 14.5 <= float(freqs[index]) < 15.5: # 15 Hz
                temp = "view"
                self.currScreen = "view"
            elif 10.5 <= float(freqs[index]) < 11.5: # 11 Hz
                temp = "rotation"
                self.currScreen = "rotation"
        elif self.currScreen == "movement":
            if 8.5 <= float(freqs[index]) < 9.5: # 9 Hz
                temp = "moveUp"
            elif 10.5 <= float(freqs[index]) < 11.5: # 11 Hz
                temp = "moveDown"
            elif 29.5 <= float(freqs[index]) < 30.5: #! 13 Hz (NEEDS TO BE CHANGED EVENTUALLY)
                temp = "moveForward"
            elif 7.5 <= float(freqs[index]) < 8.5: # 8 Hz
                temp = "moveBackward"
            elif 13.5 <= float(freqs[index]) < 14.5: # 14 Hz
                temp = "moveRight"
            elif 14.5 <= float(freqs[index]) < 15.5: # 15 Hz
                temp = "moveLeft"
        elif self.currScreen == "rotation":
            if 8.5 <= float(freqs[index]) < 9.5:
                temp = "bankUp"
            elif 10.5 <= float(freqs[index]) < 11.5:
                temp = "bankDown"
            elif 12.5 <= float(freqs[index]) < 13.5:
                temp = "rotateRight"
            elif 14.5 <= float(freqs[index]) < 15.5:
                temp = "rotateLeft"
        elif self.currScreen == "view":
            if 11.5 <= float(freqs[index]) < 12.5:
                temp = "goBack"

        self.currMovement = temp
        self.outlet.push_sample([temp]) 
        #plt.plot(freqs,magnitude)
        #plt.show()


    def plotRaw(self):
        # This doesn't do anything besides plot the input, x-axis is time, y-axis is amplitude
        plt.plot(self.x,self.y)
        plt.show()
