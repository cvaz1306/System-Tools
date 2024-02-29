import pyaudio
import numpy as np

class VirtualMicrophone:
    def __init__(self, sample_rate=44100, channels=1, chunk_size=1024):
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio_interface = pyaudio.PyAudio()
        self.stream = self.audio_interface.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            output=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self.callback
        )
        self.distortion_factor = 2.0  # Adjust the distortion factor as needed

    def callback(self, in_data, frame_count, time_info, status):
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        distorted_data = self.apply_distortion(audio_data)
        return distorted_data.tobytes(), pyaudio.paContinue

    def apply_distortion(self, audio_data):
        # Apply distortion effect
        return (audio_data * self.distortion_factor).astype(np.int16)

    def start(self):
        print("Virtual microphone with distortion started. Press Ctrl+C to stop.")
        self.stream.start_stream()

    def stop(self):
        print("Virtual microphone stopped.")
        self.stream.stop_stream()
        self.stream.close()
        self.audio_interface.terminate()

if __name__ == "__main__":
    virtual_microphone = VirtualMicrophone()
    try:
        virtual_microphone.start()
        while True:
            pass
    except KeyboardInterrupt:
        virtual_microphone.stop()
