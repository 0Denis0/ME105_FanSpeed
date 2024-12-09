import os
import pandas as pd
import numpy as np
from analyze import analyze_audio

def generate_spectra_csv(volumes_csv, data_dir, output_csv):
    """
    Generates a CSV of FFT spectra for fan speeds based on the average of the 5 quietest recordings.

    Parameters:
    - volumes_csv (str): Path to the "all_volumes.csv" file.
    - data_dir (str): Path to the root directory containing recording folders.
    - output_csv (str): Path to save the resulting "all_spectra.csv" file.
    """
    # Load the volumes CSV
    volumes_df = pd.read_csv(volumes_csv, index_col="Fan Speed")

    # Initialize a dictionary to store FFT data
    spectra_data = {}

    for fan_speed in volumes_df.index:
        # Sort folders by volume for the current fan speed and pick the 5 quietest
        sorted_volumes = volumes_df.loc[fan_speed].sort_values()
        quietest_folders = sorted_volumes.head(3).index

        print(f"Fan Speed: {fan_speed}, Quietest Folders: {list(quietest_folders)}")

        # Store magnitudes for averaging
        magnitudes_list = []

        for folder in quietest_folders:
            # Construct the path to the corresponding audio file
            audio_file = os.path.join(data_dir, folder, f"audio_{fan_speed}.wav")

            # Check if the audio file exists
            if not os.path.exists(audio_file):
                print(f"Warning: File not found: {audio_file}")
                continue

            # Analyze the audio file
            _, freqs, fft_magnitude = analyze_audio(audio_file)

            # Filter frequencies up to 3500 Hz
            mask = freqs <= 3500
            magnitudes_list.append(fft_magnitude[mask])

        if not magnitudes_list:
            print(f"No valid audio files found for fan speed {fan_speed}.")
            continue

        # Calculate the average magnitude
        average_magnitude = np.mean(magnitudes_list, axis=0)

        # Store the result in the dictionary
        spectra_data[fan_speed] = average_magnitude

    # Convert the spectra data to a DataFrame
    freqs_up_to_3500 = freqs[mask]
    spectra_df = pd.DataFrame(spectra_data, index=freqs_up_to_3500)
    spectra_df.index.name = "Frequency (Hz)"

    # Save the DataFrame to a CSV file
    spectra_df.to_csv(output_csv)
    print(f"Spectrum data saved to {output_csv}")


volumes_csv = "data3//all_volumes.csv"
data_dir = "data3"
output_csv = "data3//all_spectra.csv"
generate_spectra_csv(volumes_csv, data_dir, output_csv)
