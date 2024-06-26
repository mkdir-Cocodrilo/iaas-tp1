import os
import pandas as pd

def read_all_csv_files(directory):
    """Reads all CSV files in the specified directory and returns a list of DataFrames."""
    dataframes = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            dataframes.append(df)
    return dataframes
