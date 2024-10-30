import os
import time
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write

def record_audio(filename, duration=10, sample_rate=44100):
    """
    Records an audio clip and saves it with the given filename.

    Parameters:
    - filename (str): The name of the file to save the audio as (e.g., 'output.wav').
    - duration (int): The duration of the recording in seconds. Default is 10 seconds.
    - sample_rate (int): The sample rate for recording. Default is 44100 Hz.
    """
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait for the recording to complete
    write(filename, sample_rate, audio_data)  # Save as .wav file
    print(f"Recording saved to {filename}")

def create_recordings_folder():
    # Create a folder to save recordings with current date and time
    folder_name = f"data\\Recordings_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def recording_script():
    folder_name = create_recordings_folder()
    values = list(range(100, -1, -1))
    text_file = "C:\\Users\\Denis\\Downloads\\Apps\\FanControl\\Configurations\\testing.sensor"

    for value in values:
        # Write the current value to the text file
        with open(text_file, 'w') as file:
            file.write(str(value))
        
        print(f"Value {value} written to {text_file}")
        
        # Wait for 3 seconds
        time.sleep(3)
        
        # Record audio with the value as part of the filename
        filename = os.path.join(folder_name, f"audio_{value}.wav")
        record_audio(filename, duration=5)

if __name__ == "__main__":
    while True:
        recording_script()



