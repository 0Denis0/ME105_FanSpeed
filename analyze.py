import os
import re
import pandas as pd
import seaborn as sns
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

def analyze_folder(folder_path):
    values = []
    volumes = []
    spectral_data = []
    
    # Iterate over all .wav files in the folder
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".wav"):
            # Extract the value from the filename using regex
            match = re.search(r"audio_(\d+).wav", filename)
            if match:
                value = int(match.group(1))
                values.append(value)
                
                # Perform analysis on the audio file
                file_path = os.path.join(folder_path, filename)
                print(f"Analyzing audio recording for fan speed {value}")
                average_volume, freqs, fft_magnitude = analyze_audio(file_path)
                
                volumes.append(average_volume)
                spectral_data.append(fft_magnitude)

    # Save data to a CSV file
    csv_file = os.path.join(folder_path, "analysis_results.csv")
    df = pd.DataFrame({
        "Value": values,
        "Average Volume": volumes,
    })
    df.to_csv(csv_file, index=False)
    print(f"Analysis results saved to {csv_file}")

    # Save spectral data separately in a .npz file
    npz_file = os.path.join(folder_path, "spectral_data.npz")
    np.savez(npz_file, values=values, freqs=freqs, spectral_data=spectral_data)
    print(f"Spectral data saved to {npz_file}")

    # plotVolumes(values, volumes) # Create the Value vs Volume plot
    # plotSpectra(values, freqs, spectral_data) # Create the spectral distribution heatmap
    

def plotVolumes(values, volumes):
    plt.figure(figsize=(10, 5))
    plt.plot(values, volumes, marker='o')
    plt.xlabel("Value")
    plt.ylabel("Average Volume")
    plt.title("Value vs Average Volume")
    plt.grid()
    plt.show()

def plotSpectra(values, freqs, spectal_data):
    spectral_data = np.array(spectral_data)
    plt.figure(figsize=(12, 8))
    sns.heatmap(spectral_data.T, xticklabels=values, yticklabels=freqs, cmap="viridis", cbar_kws={'label': 'Magnitude'})
    plt.xlabel("Value")
    plt.ylabel("Frequency (Hz)")
    plt.title("Spectral Distribution Heatmap")
    plt.show()

def analyze_audio(file_path):
    # Read the .wav file
    sample_rate, data = wavfile.read(file_path)
    
    # If the audio has two channels (stereo), convert it to mono by averaging the channels
    if len(data.shape) == 2:
        data = data.mean(axis=1)
    
    # Calculate the average volume (magnitude)
    average_volume = np.mean(np.abs(data))

    # Perform Fourier Transform to get the spectral distribution
    n = len(data)
    freqs = np.fft.rfftfreq(n, d=1/sample_rate)
    fft_magnitude = np.abs(np.fft.rfft(data)) / n

    return average_volume, freqs, fft_magnitude

# def plotFromFile(folder_path):
#     plotVolumes()
#     plotSpectra()

if __name__ == "__main__":
    # folder_path = "data\\Recordings_20241029_195328"  # Update with your folder path
    data_path = "data3"
    folders = [os.path.join(data_path, folder) for folder in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, folder))]
    for folder in folders:
        analyze_folder(folder)
        print(f"Finished analysis of {folder}")

    zero, _, _ = analyze_audio("dataSilence//Recordings_20241209_092922//audio_1.wav")
    print(f"Zero reference: {zero}")
