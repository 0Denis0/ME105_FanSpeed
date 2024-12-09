import os
import pandas as pd

def aggregate_volumes(data_dir, output_csv):
    """
    Aggregates volume values from 'analysis_results.csv' across multiple folders.

    Parameters:
    - data_dir (str): Path to the root directory containing folders with 'analysis_results.csv'.
    - output_csv (str): Path to save the aggregated CSV file.
    """
    aggregated_data = {}  # Dictionary to store fan speeds and their volume values
    folder_names = []      # Counter for trials (folders)

    # Iterate through each folder in the data directory
    for folder in sorted(os.listdir(data_dir)):
        folder_path = os.path.join(data_dir, folder)
        analysis_file = os.path.join(folder_path, "analysis_results.csv")

        # Check if 'analysis_results.csv' exists in the folder
        if os.path.isdir(folder_path) and os.path.exists(analysis_file):
            print(f"Found analysis file: {analysis_file}")
            folder_names.append(folder)  # Add folder name as a column

            # Read the CSV file
            df = pd.read_csv(analysis_file)

            # Ensure it contains the expected columns
            if 'Value' in df.columns and 'Average Volume' in df.columns:
                for _, row in df.iterrows():
                    fan_speed = int(row['Value'])
                    volume = row['Average Volume']

                    # Initialize the fan speed entry if not present
                    if fan_speed not in aggregated_data:
                        aggregated_data[fan_speed] = {}

                    # Append the volume to the corresponding fan speed
                    aggregated_data[fan_speed][folder] = volume
            else:
                print(f"Skipping {analysis_file}: Missing required columns.")
        else:
            print(f"Skipping {folder}: 'analysis_results.csv' not found.")

   
    # Create a DataFrame from the aggregated data
    df_aggregated = pd.DataFrame.from_dict(aggregated_data, orient='index')
    df_aggregated.index.name = "Fan Speed"

    # Ensure all columns (folder names) are present, even if some fan speeds are missing
    df_aggregated = df_aggregated.reindex(columns=folder_names)

    # Save the aggregated data to a CSV file
    df_aggregated.to_csv(output_csv)
    print(f"Aggregated data saved to {output_csv}")


data_dir = "data3"  # Replace with your data directory
output_csv = data_dir + "//all_volumes.csv"  # Desired output file name
aggregate_volumes(data_dir, output_csv)
