import os
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.io import wavfile

def compute_fft_magnitude(file_path):
    """
    Computes the FFT magnitude spectrum for a .wav file.
    Returns the frequency bins and corresponding magnitudes.
    """
    sample_rate, data = wavfile.read(file_path)
    
    # Convert to mono if stereo
    if len(data.shape) == 2:
        data = data.mean(axis=1)
    
    # Compute FFT
    n = len(data)
    fft_magnitude = np.abs(np.fft.rfft(data)) / n
    freqs = np.fft.rfftfreq(n, d=1/sample_rate)
    
    return freqs, fft_magnitude

def analyze_folder_spectrogram(folder_path):
    fan_speeds = []
    spectra = {}

    # Loop through each .wav file in the specified folder
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".wav"):
            # Extract fan speed from filename
            match = re.search(r"audio_(\d+).wav", filename)
            if match:
                fan_speed = int(match.group(1))
                file_path = os.path.join(folder_path, filename)
                
                # Compute FFT and store the spectrum
                freqs, fft_magnitude = compute_fft_magnitude(file_path)
                
                # Add the fan speed and spectrum data
                fan_speeds.append(fan_speed)
                spectra[fan_speed] = fft_magnitude

    # Sort fan speeds and reformat spectra data for plotting
    fan_speeds = sorted(spectra.keys())
    spectrum_matrix = np.array([spectra[speed] for speed in fan_speeds])

    # Create spectrogram plot
    plt.figure(figsize=(12, 8))
    sns.heatmap(spectrum_matrix.T, xticklabels=fan_speeds, yticklabels=freqs, cmap="viridis", cbar_kws={'label': 'Intensity'})
    plt.xlabel("Fan Speed")
    plt.ylabel("Frequency (Hz)")
    plt.title("Spectrogram by Fan Speed")
    plt.show()

if __name__ == "__main__":
    folder_path = "data2\\Recordings_20241031_001603"  # Replace with the path to your folder
    # analyze_folder_spectrogram(folder_path)
    # spectrogram = []
    # for recording in sorted(os.listdir(folder_path)):
    #     if recording.endswith(".wav"):
    #         print(f"analyzing {recording}")
    #         freqs, magnitudes = compute_fft_magnitude(folder_path + "\\audio_75.wav")
    #         spectrogram.append(magnitudes)
    
    # spectrogram = np.array(spectrogram).T
    # print(f"width: {len(spectrogram)}")
    # print(f"length: {len(spectrogram[0])}")
    # fig = plt.figure(99)
    # ax = fig.add_subplot(111,aspect='equal')
    # plt.imshow(spectrogram, aspect='equal')
    # ratio = 1.0
    # xleft, xright = ax.get_xlim()
    # ybottom, ytop = ax.get_ylim()
    # ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    # plt.show()

    data = []

    for recording in sorted(os.listdir(folder_path)):
        if recording.endswith(".wav"):
            print(f"analyzing {recording}")
            sample_rate, tempData = wavfile.read(folder_path + "\\" + recording)
            data = data + list(tempData)
            
    #sample_rate, data = wavfile.read("data2\Recordings_20241031_001603\\audio_75.wav")
    plt.specgram(data, Fs=sample_rate, NFFT=21, noverlap=0, scale='dB')
    plt.show()

