"""
Name: Chi Thieu
Course: ISTA 131
"""
import numpy as np
import pandas as pd
from datetime import datetime

# Function to get data from the CSV file
def get_data():
    # Read the CSV file with specific parameters
    df = pd.read_csv('N_seaice_extent_daily_v3.0.csv', skiprows=2, names=[0, 1, 2, 'Extent'], usecols=[0, 1, 2, 3], parse_dates={'Dates': [0, 1, 2]}, header=None)
    # Set 'Dates' column as index
    s = df['Extent']
    s.index = df['Dates']
    # Reindex the series to fill missing dates
    return s.reindex(pd.date_range(s.index[0], s.index[-1]))

# Function to clean the data by filling NaN values
def clean_data(series):
    # Fill NaN values with the mean of the two adjacent days from the previous and following year
    for i in range(len(series)):
        if pd.isnull(series[i]):
            series[i] = (series[i - 1] + series[i + 1]) / 2
    # Fill remaining NaN values with the mean of the same day from the previous and following year
    for i in range(len(series)):
        if pd.isnull(series[i]):
            series[i] = (series[i - 365] + series[i + 366]) / 2

# Function to get column labels for the DataFrame
def get_column_labels():
    # Generate date range from January 1, 1979, to December 31, 1979, and format as 'mmdd'
    a = pd.date_range('1979-01-01', '1979-12-31').strftime('%m%d').tolist()
    return a

# Function to extract DataFrame from the cleaned series
def extract_df(series):
    # Create index range from 1979 to 2023 and column labels with 'mmdd' format
    newdf = range(1979, 2024)
    df = pd.DataFrame(index=newdf, columns=get_column_labels(), dtype=np.float64)
    # Fill DataFrame with values from the series based on datetime index
    for row in df.index:
        for col in df.columns:
            x = datetime(row, int(col[:2]), int(col[2:]))
            df.loc[row, col] = series[x]
    return df

# Function to extract data for the year 2024
def extract_2024(series):
    return series.loc[datetime(2024, 1, 1):]

# Main function
def main():
    # Get the data series
    a = get_data()
    # Clean the data
    clean_data(a)
    # Extract DataFrame for years 1979-2023 and save as CSV
    extract_df(a).to_csv('data_79_23.csv')
    # Extract data for year 2024 and save as CSV
    extract_2024(a).to_csv('data_2024.csv', header=False)

# Entry point of the program
if __name__ == '__main__':
    main()
