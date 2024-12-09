import os
import pandas as pd
import numpy as np

from analyze import analyze_audio

def generate_spectra_csv(volumes_csv, data_dir, output_csv):
    """
    Generates a CSV of FFT spectra for fan speeds based on the lowest volume recordings.

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
        # Find the folder (column) with the lowest volume for the current fan speed
        lowest_volume = volumes_df.loc[fan_speed].min()
        folder_with_lowest_volume = volumes_df.loc[fan_speed].idxmin()

        print(f"Fan Speed: {fan_speed}, Lowest Volume: {lowest_volume}, Folder: {folder_with_lowest_volume}")

        # Construct the path to the corresponding audio file
        audio_file = os.path.join(data_dir, folder_with_lowest_volume, f"audio_{fan_speed}.wav")

        # Check if the audio file exists
        if not os.path.exists(audio_file):
            print(f"Warning: File not found: {audio_file}")
            continue

        # Analyze the audio file
        average_volume, freqs, fft_magnitude = analyze_audio(audio_file)

        # Filter frequencies up to 5000 Hz and store FFT magnitudes
        mask = freqs <= 3500
        spectra_data[fan_speed] = fft_magnitude[mask]

    # Convert the spectra data to a DataFrame
    freqs_up_to_5000 = freqs[mask]
    spectra_df = pd.DataFrame(spectra_data, index=freqs_up_to_5000)
    spectra_df.index.name = "Frequency (Hz)"

    # Save the DataFrame to a CSV file
    spectra_df.to_csv(output_csv)
    print(f"Spectrum data saved to {output_csv}")


volumes_csv = "data3//all_volumes.csv"
data_dir = "data3"
output_csv = "data3//all_spectra.csv"
generate_spectra_csv(volumes_csv, data_dir, output_csv)
