import os
import pandas as pd
import matplotlib.pyplot as plt

data_path = "data2"
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

# Scatter plot of Value vs Average Volume
plt.figure(figsize=(10, 6))
plt.scatter(all_data["Value"], all_data["Average Volume"], marker=".")
plt.xlabel("Value")
plt.ylabel("Average Volume")
plt.title("Combined Scatter Plot of Value vs Average Volume")
plt.grid(True)
plt.show()
