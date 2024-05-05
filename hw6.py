"""
Name: Chi Thieu
Course: ISTA 131
"""
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Function to get column labels for the dataframe
def get_column_labels():
    # Generate date range from January 1, 1979, to December 31, 1979, and format as 'mmdd'
    a = pd.date_range('1979-01-01', '1979-12-31').strftime('%m%d').tolist()
    return a

# Function to extract data for the year 2024 from a CSV file
def get_2024():
    # Read the data from 'data_2024.csv' without header
    dataframe = pd.read_csv('data_2024.csv', header=None)
    # Get column labels
    columns = get_column_labels()
    # Use first part of column labels as index
    index = columns[:len(dataframe)]
    # Return a Series with values from 'data_2024.csv' and index from column labels
    return pd.Series(dataframe[1].values, index)

# Function to extract frame for figure 1
def extract_fig_1_frame(dataframe):
    # Create an empty DataFrame with columns from input dataframe
    dataframe_1 = pd.DataFrame(index=["mean", "two_s"], columns=dataframe.columns)
    # Calculate mean and two times standard deviation for each column
    for columns in dataframe.columns:
        dataframe_1.loc["mean", columns] = dataframe[columns].mean()
        dataframe_1.loc["two_s", columns] = dataframe[columns].std() * 2
    return dataframe_1

# Function to extract frame for figure 2
def extract_fig_2_frame(dataframe):
    # Create a list to store mean values for each decade
    data = []
    # Calculate mean values for each decade and append to the list
    data.append(dataframe.loc[1980:1989].mean())
    data.append(dataframe.loc[1990:1999].mean())
    data.append(dataframe.loc[2000:2009].mean())
    data.append(dataframe.loc[2010:2019].mean())
    # Define index for the DataFrame
    index = ["1980s", "1990s", "2000s", "2010s"]
    return pd.DataFrame(data, index, dataframe.columns)

# Function to create figure 1
def make_fig_1(first_dataframe, second_dataframe):
    # Get the current axis
    axis = plt.gca()
    # Plot mean values
    first_dataframe.loc['mean'].plot(label='mean')
    # Plot data for 2021 as dashed line
    second_dataframe.loc[2012].plot(linestyle='dashed', label='2021')
    # Plot data for 2024
    get_2024().plot(label='2024')
    # Set x-axis tick labels
    xtl = [tick_label.get_text() for tick_label in axis.get_xticklabels()]
    axis.set_xticklabels(xtl)
    # Calculate y-axis values for shading
    x = np.arange(365)
    y1 = (first_dataframe.loc['mean'] + first_dataframe.loc['two_s']).values.astype(float)
    y2 = (first_dataframe.loc['mean'] - first_dataframe.loc['two_s']).values.astype(float)
    # Fill between mean + 2 std devs and mean - 2 std devs
    plt.fill_between(x, y1, y2, label="$\pm$2 std devs", color="lightgray")
    # Set labels and legend
    plt.ylabel("NH Sea Ice Extent ($10^6$ km$^2$)", fontsize=24)
    plt.legend(loc="upper right")

# Function to create figure 2
def make_fig_2(plot_dataframe):
    # Get the current axis
    axis = plt.gca()
    # Plot mean values for each decade as dashed lines
    plot_dataframe.loc['1980s'].plot(linestyle='dashed', label='1980s')
    plot_dataframe.loc['1990s'].plot(linestyle='dashed', label='1990s')
    plot_dataframe.loc['2000s'].plot(linestyle='dashed', label='2000s')
    plot_dataframe.loc['2010s'].plot(linestyle='dashed', label='2010s')
    # Plot data for 2024
    get_2024().plot(label='2024')
    # Set x-axis tick labels
    xtl = ["1", "0101", "0220", "0411", "0531", "0720", "0908", "1028", "1217", "1"]
    axis.set_xticklabels(xtl)
    # Set labels and legend
    plt.ylabel("NH Sea Ice Extent ($10^6$ km$^2$)", fontsize=24)
    plt.legend(loc='lower left')

# Main function
def main():
    # Read the data from 'data_79_23.csv' and set the first column as index
    csv_filename = pd.read_csv('data_79_23.csv', index_col=0)
    # Extract frame for figure 1
    first_dataframe = extract_fig_1_frame(csv_filename)
    # Extract frame for figure 2
    second_dataframe = extract_fig_2_frame(csv_filename)
    # Create figure 1
    make_fig_1(first_dataframe, csv_filename)
    # Create a new figure for figure 2
    plt.figure()
    # Create figure 2
    make_fig_2(second_dataframe)
    # Show the plots
    plt.show()

# Entry point of the program
if __name__ == '__main__':
    main()
