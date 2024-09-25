import threading
from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
from myFFT import FFT

#This script contains the FFT part while main does not
class Main_Controller:
    def __init__(self) -> None:
        # pullEEG is a variable that can be accessed both by the EEG Stream and the Marker stream so that we can manipulate and look at it at any time
        self.pullEEG = False
        self.eeg_stream = None
        self.marker_stream = None
        self.FFT = None

    def run_eeg(self):
        # Using the inner class EEG_Stream we create the object that will stream the EEG data
        self.eeg_stream = self.EEG_Stream(self)
        self.eeg_stream.find_stream()
        self.eeg_stream.listen()
        

    def run_marker(self):
        # Using the inner class Marker_Stream we create the object that will stream the Markers
        self.marker_stream = self.Marker_Stream(self)
        self.marker_stream.find_stream()
        self.marker_stream.listen()
        

    def run_all(self):
        # Initialize FFT object, currently does not have any information on the timestamps or eeg data, will add later
        # It is absolutely vital that this is run prior to connecting to stream on Godot
        self.FFT = FFT()
        # Makes sure user is ready to move on
        while True:
            userinput = input("Please type \"c\" to connect\n")
            if userinput.lower() == "c":
                break
            else:
                print("Invalid input, type \"c\" to connect")
        # Here we use multi-threading so that we can stream both the EEG data as well as the Markers at the same time
        script1_thread = threading.Thread(target=self.run_eeg)
        script2_thread = threading.Thread(target=self.run_marker)

        script1_thread.start()
        script2_thread.start()

        script1_thread.join()
        script2_thread.join()

    class EEG_Stream:
        # This is the EEG_Stream Object that will be in charge of streaming solely the EEG data
        # We will only pull EEG data when the pullEEG outerclass variable is true as that will be our indicator of when we should or should not pull

        def __init__(self,outer) -> None:
            # The outer is a reference to the outerclass, the pullEEG_EEG is this objects personal variable keeping track of whether or not we should
            # pull the EEG data or not. This personal variable will be changed depending on the outerclass' version of this variable (pullEEG)

            self.inlet = None
            self.pullEEG_EEG = False
            self.outer = outer
        
        def find_stream(self):
            # This looks for the stream of type EEG and makes sure the name is "droneEEG". It is basically what connects to the EEG Stream
            print("looking for eeg stream...")
            streams = resolve_stream('type', 'EEG')
            for stream in streams:
                if stream.name() == "droneEEG":
                    self.inlet = StreamInlet(stream)
                    break
            #inlet = StreamInlet(stream[0])

        def get_pullEEG(self):
            # This sets this object's personal version of the pullEEG variable to what ever the outerclass' variable is
            self.pullEEG_EEG = self.outer.pullEEG
        
        def listen(self):
            # This is an endless loop that constantly listens, reading the EEG data (so long as pullEEG_EEG is True)
            while True:
                # calls method to check current status of pullEEG
                self.get_pullEEG()
                if self.pullEEG_EEG == True:
                    sample, timestamp = self.inlet.pull_sample()
                    # This continuously adds a timestamp and sample to the list holding the eeg data and timestamps which will later be used in an FFT
                    self.outer.FFT.addTimestamp(timestamp)
                    self.outer.FFT.addAmplitude(sample[0]) #! ARBITRARY CHANNEL, MAKE SURE TO INCLUDE OTHERS
                    #print(sample,timestamp)
    
    class Marker_Stream:
        # This is the Marker_Stream Object that will be in charge of looking at the incoming Markers, it will then change the pullEEG outerclass variable so that we know when to
        # start pulling EEG data with the EEG_Stream object and when to stop

        def __init__(self,outer) -> None:
            # This, just like the EEG_Stream keeps a reference to the outerclass as well as its own personal pullEEG variable (pullEEG_Marker).
            # We will be manipulating both pullEEG variables as it is dependent on the markers that come in for whether or not we should be gathering data
            self.pullEEG_Marker = False
            self.inlet = None
            self.outer = outer

        def find_stream(self):
            # This just connects to the stream of type Markers, make sure the incoming marker stream name is set to "GodotMarkerStream"
            print("looking for a marker stream...")
            streams = resolve_stream("type", "Markers")
            for stream in streams:
                if stream.name() == "GodotMarkerStream":
                    self.inlet = StreamInlet(stream)
                    break

        def set_pullEEG(self):
            # This is where we change the outerclass' version of pullEEG so that the EEG_Stream object will start streaming the EEG data or stop streaming
            self.outer.pullEEG = self.pullEEG_Marker
        
        def listen(self):
            # Endless loop of gathering markers as we always need to know if we should be streaming the EEG data or not
            while True:

                #continuously gather the sample as well as the particular timestamp
                sample, timestamp = self.inlet.pull_sample()
                # If the marker says to start, start gathering data, if it says to stop, stop gathering
                if sample[0] == "Start Gathering Data":
                    self.pullEEG_Marker = True
                elif sample[0] == "Stop Gathering Data":
                    self.pullEEG_Marker = False
                    # If the list holding the EEG data is not empty, then perform the FFT and afterwards wipe the list of EEG data and list of timestamps for the next iteration of this
                    if self.outer.FFT.x:
                        self.outer.FFT.transform()
                        self.outer.FFT.setTimestamps([])
                        self.outer.FFT.setAmplitude([])
                
                print("got %s at time %s" % (sample[0], timestamp))
                # Calls method to set the pullEEG variable
                self.set_pullEEG()

if __name__ == "__main__":
    control = Main_Controller()
    control.run_all()


    #print("hi")
