import threading
from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo
from myFFT import FFT

class Calibrator:
    def __init__(self) -> None:
        self.freq_map = {}
        self.FFT = FFT()
        self.EEGinlet = None
        self.Markerinlet = None
        self.collect_data = False
        self.start_freq = 6 # This is the first frequency that gets calibrated, the listen_Marker function will start here and incrememnt by 1 until it reaches end_freq
        self.end_freq = 97
        self.stop_threads = False

    def connect_marker_stream(self):
        print("looking for Marker stream...")
        streams = resolve_stream('type', 'Markers')
        for stream in streams:
            if stream.name() == "GodotMarkerStream":
                self.Markerinlet = StreamInlet(stream)
                break

    def connect_eeg_stream(self):
        print("looking for EEG stream...")
        streams = resolve_stream('type', 'EEG')
        for stream in streams:
            if stream.name() == "droneEEG":
                self.EEGinlet = StreamInlet(stream)
                break

    def listen_EEG(self):
        #print("test")
        while (not self.stop_threads):
            #continuously gather the sample as well as the particular timestamp
            sample, timestamp = self.EEGinlet.pull_sample()
            if self.collect_data:
                self.FFT.addAmplitude(sample)
                self.FFT.addTimestamp(timestamp)


    def listen_Marker(self):
        cur_freq = self.start_freq
        while (not self.stop_threads):
            #continuously gather the sample as well as the particular timestamp
            sample, timestamp = self.Markerinlet.pull_sample()
            if sample[0] == "Start Calibrating":
                self.collect_data = True
            elif sample[0] == "Stop Calibrating":
                self.collect_data = False
                if cur_freq not in self.freq_map:
                    self.freq_map[cur_freq] = []
                self.freq_map[cur_freq].append(self.FFT.compute_FFT())
                self.FFT.setAmplitude([])
                self.FFT.setTimestamps([])
                self.collect_data = False
                cur_freq += 1
                if cur_freq == self.end_freq:
                    self.stop_threads = True
            elif sample[0] == "Calibration Complete":
                self.stop_threads = True

    def calibrate(self):
        self.connect_eeg_stream()
        self.connect_marker_stream()
        print("Proceed to Calibrate")
        eeg_thread = threading.Thread(target=self.listen_EEG)
        marker_thread = threading.Thread(target=self.listen_Marker)

        eeg_thread.start()
        marker_thread.start()

        eeg_thread.join()
        marker_thread.join()
        print(self.freq_map)
        return self.freq_map

        

    