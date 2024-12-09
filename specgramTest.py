import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils import cmap_map
from analyze import analyze_audio

def plot_spectra_with_db(spectra_csv, output_image):
    """
    Plots the spectrum data as an image with fan speed on the x-axis and frequency on the y-axis,
    converting magnitudes to decibel ratios (dB) relative to zero noise reference.

    Parameters:
    - spectra_csv (str): Path to the "all_spectra.csv" file.
    - output_image (str): Path to save the output image.
    """
    # Load the spectra data
    spectra_df = pd.read_csv(spectra_csv, index_col="Frequency (Hz)")

    # Prepare the output data structure
    fan_speeds = sorted([int(col) for col in spectra_df.columns])  # Ascending fan speeds
    frequencies = spectra_df.index.to_numpy()
    max_frequency = int(frequencies.max()) + 1

    # Initialize arrays to hold binned spectrum data
    binned_spectra = np.zeros((max_frequency, len(fan_speeds)))
    bin_counts = np.zeros(max_frequency)  # To count how many values contribute to each bin

    # Analyze zero noise reference
    zeroVol, zfreqs, zAmps = analyze_audio("dataSilence//Recordings_20241209_092922//audio_1.wav")

    # Bin the zero noise amplitudes
    binned_zAmps = np.zeros(max_frequency)
    for freq, amplitude in zip(zfreqs, zAmps):
        bin_index = int(freq)  # Integer frequency bins
        if bin_index < max_frequency:
            binned_zAmps[bin_index] += amplitude
            bin_counts[bin_index] += 1

    # Normalize the binned zero noise reference
    bin_counts[bin_counts == 0] = 1  # Avoid division by zero
    binned_zAmps /= bin_counts

    # Process each fan speed column
    for i, fan_speed in enumerate(fan_speeds):
        spectrum = spectra_df[str(fan_speed)].to_numpy()

        # Bin the spectrum into integer frequency increments
        for freq, magnitude in zip(frequencies, spectrum):
            bin_index = int(freq)  # Integer frequency bins
            if bin_index < max_frequency:
                binned_spectra[bin_index, i] += magnitude

    # Convert summed magnitudes to averages and calculate dB ratios
    averaged_spectra = binned_spectra / bin_counts[:, None]
    spectra_db = 20 * np.log10((averaged_spectra + 1e-12) / (binned_zAmps[:, None] + 1e-12))

    # Trim the array to only include bins with data
    used_bins = np.any(spectra_db > -np.inf, axis=1)
    spectra_db = spectra_db[used_bins, :]
    binned_frequencies = np.arange(max_frequency)[used_bins]

    # Plot the spectrum as an image
    plt.figure(figsize=(10, 8))
    plt.imshow(
        spectra_db,
        aspect="auto",
        cmap="viridis",
        extent=[min(fan_speeds), max(fan_speeds), binned_frequencies[0], binned_frequencies[-1]],
        origin="lower",  # Makes frequencies increase going upwards
    )
    plt.colorbar(label="Power Ratio (dB)")
    plt.xlabel("Fan Speed")
    plt.ylabel("Frequency (Hz)")
    plt.title("Spectra Heatmap in dB (Relative to Zero Noise)")
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig(output_image)
    plt.close()
    print(f"Spectra plot saved to {output_image}")


# Example usage
spectra_csv = "data3//all_spectra.csv"
output_image = "data3//avgSpectra_plot_db.png"
plot_spectra_with_db(spectra_csv, output_image)
