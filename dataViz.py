import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_path = "data3"
folders = [os.path.join(data_path, folder) for folder in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, folder))]

# Initialize an empty list to collect data from all folders
combined_data = []

for folder in folders:
    csv_path = os.path.join(folder, "analysis_results.csv")  # Assuming each folder has a CSV named 'analysis_results.csv'
    
    if os.path.exists(csv_path):
        # Read the CSV, ignoring the header, and add to the combined data
        df = pd.read_csv(csv_path)
        combined_data.append(df)


# Combine all dataframes into one
all_data = pd.concat(combined_data, ignore_index=True)

# Calculate the statistics for each fan speed
grouped = all_data.groupby("Value")["Average Volume"]
min_volumes = grouped.min()
q25_volumes = grouped.quantile(0.25)
median_volumes = grouped.median()
q75_volumes = grouped.quantile(0.75)

# Scatter plot of Value vs Average Volume
plt.figure(figsize=(10, 6))
plt.scatter(all_data["Value"], 20 * np.log10(all_data["Average Volume"]), marker=".", alpha=0.6, label="All Data")

# Plot the calculated curves
plt.plot(min_volumes.index, 20 * np.log10(min_volumes.values), color="red", label="Minimum")
# plt.plot(q25_volumes.index, 20 * np.log10(q25_volumes.values), color="orange", label="25th Percentile")
# plt.plot(median_volumes.index, 20 * np.log10(median_volumes.values), color="green", label="Median")
# plt.plot(q75_volumes.index, 20 * np.log10(q75_volumes.values), color="blue", label="75th Percentile")


# Set axis limits and move the legend
plt.xlim(-1, 101)
plt.ylim(31, 43)
plt.legend(loc="upper left")

# Add labels, title, and grid
plt.xlabel("Fan Speed (%)")
plt.ylabel("Average Volume (dB)")
plt.title("Computer Fan Speed vs Average Volume of Emitted Noise")
plt.grid(True)
plt.show()


# 3D histogram
from mpl_toolkits.mplot3d import Axes3D  # Import for 3D plotting

# Create a new figure for the 3D histogram
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Prepare data for the histogram
x_data = all_data["Value"]
y_data = 20 * np.log10(all_data["Average Volume"])

# Create histogram bins
x_bins = np.arange(0, 101, 1)  # Bins for fan speed
y_bins = np.linspace(30, 44, num=20)  # Bins for volume in dB

# Compute the histogram
hist, x_edges, y_edges = np.histogram2d(x_data, y_data, bins=[x_bins, y_bins])

# Generate x, y, and z positions for the bars
x_pos, y_pos = np.meshgrid(x_edges[:-1], y_edges[:-1], indexing="ij")
x_pos = x_pos.ravel()
y_pos = y_pos.ravel()
z_pos = np.zeros_like(x_pos)

# Flatten the histogram and determine bar sizes
dx = dy = np.diff(x_bins)[0]  # Uniform bin widths for x and y
dz = hist.ravel()  # Heights of the bars

# Plot the 3D histogram
ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, zsort='average', shade=True, color=plt.cm.viridis(dz / dz.max()))


# Add labels and title
ax.set_xlabel("Fan Speed (%)")
ax.set_ylabel("Average Volume (dB)")
ax.set_zlabel("Frequency")
ax.set_title("3D Histogram of Fan Speed vs. Average Volume")

# Show the plot
plt.show()
