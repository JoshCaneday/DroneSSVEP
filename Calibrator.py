from pylsl import StreamInlet, resolve_stream, StreamOutlet, StreamInfo

class Calibrator:
    def __init__(self) -> None:
        self.freq_map = {}
        self.inlet = None

    def connect_marker_stream(self):
        print("looking for Marker stream...")
        streams = resolve_stream('type', 'Marker')
        for stream in streams:
            if stream.name() == "calibrationMarkerStream":
                self.inlet = StreamInlet(stream)
                break

    def connect_eeg_stream(self):
        print("looking for EEG stream...")
        streams = resolve_stream('type', 'EEG')
        for stream in streams:
            if stream.name() == "calibrationEEGStream":
                self.inlet = StreamInlet(stream)
                break

    def calibrate(self, frequency):
        pass

    