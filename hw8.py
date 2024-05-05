"""
Name: Chi Thieu
Course: ISTA 131
"""
import json
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to perform sentiment analysis on tweets from a file
def get_sentiment(file_name):
    # Load tweets from the file
    with open(file_name, 'r') as file:
        tweets = json.load(file)
    
    # Perform sentiment analysis on each tweet and store the results
    sentiments = []
    for tweet_text in tweets:
        analysis = TextBlob(tweet_text)
        # Check if the sentiment polarity and subjectivity are not both 0.0
        if analysis.sentiment.polarity != 0.0 or analysis.sentiment.subjectivity != 0.0:
            sentiments.append(analysis.sentiment.polarity)
    
    # Calculate the mean polarity and the sample standard deviation
    if sentiments:  # Check if the list is not empty
        mean_polarity = np.mean(sentiments)
        std_dev_polarity = np.std(sentiments, ddof=1)  # ddof=1 for sample standard deviation
        return [mean_polarity, std_dev_polarity]
    else:
        return [0, 0]

# Function to create a DataFrame with sentiment analysis results
def get_ct_sentiment_frame():
    data = {'Trump': {'1/29': get_sentiment('trump_240129_519pm.json'),'1/30': get_sentiment('trump_240130_1139am.json')},
            'Biden': {'1/29': get_sentiment('biden_240129_519pm.json'),'1/30': get_sentiment('biden_240130_1139am.json')}}
    
    # Initialize a list to hold the data for DataFrame creation
    rows_list = []
    
    # Loop through each candidate and date to create a data dictionary for each row
    for candidate, dates in data.items():
        data_dict = {'Candidate': candidate}
        for date, stats in dates.items():
            data_dict[f'{date} mean'] = stats[0]
            data_dict[f'{date} std'] = stats[1]
        rows_list.append(data_dict)
    
    # Create DataFrame from the list and set the index
    df = pd.DataFrame(rows_list)
    df.set_index('Candidate', inplace=True)
    df.index.name = None
    return df

# Function to create the figure based on sentiment frame data
def make_fig(sentiment_frame):
    # Check if the sentiment frame is None or empty
    if sentiment_frame is None or sentiment_frame.empty:
        return
    
    # Create the figure
    plt.figure(figsize=(10, 6))
    plt.gcf().set_facecolor('black')
    plt.gca().set_facecolor('#FFE5E5')
    
    n_groups = 2
    index = np.linspace(0.2, 0.8, n_groups)
    bar_width = 0.12 
    
    # Extract means and standard deviations for Trump and Biden
    trump_means = sentiment_frame.loc['Trump', ['1/29 mean', '1/30 mean']].values
    biden_means = sentiment_frame.loc['Biden', ['1/29 mean', '1/30 mean']].values
    trump_stds = sentiment_frame.loc['Trump', ['1/29 std', '1/30 std']].values
    biden_stds = sentiment_frame.loc['Biden', ['1/29 std', '1/30 std']].values
    
    # Plot bars for Trump and Biden with error bars representing standard deviations
    trump_bars = plt.bar(index - bar_width/2, trump_means, bar_width, yerr=trump_stds, color='blue', edgecolor='black', capsize=5, 
                          error_kw={'elinewidth':1.5, 'capthick':1})
    biden_bars = plt.bar(index + bar_width/2, biden_means, bar_width, yerr=biden_stds, color='green', edgecolor='black', capsize=5, 
                          error_kw={'elinewidth':1.5, 'capthick':1})
    
    # Set spine color to red
    for spine in plt.gca().spines.values():
        spine.set_color('red')
    
    # Set labels, ticks, and formatting
    plt.xticks(index, ['Trump-Biden 01/29', 'Trump-Biden 01/30'], fontsize=18, color='red')
    plt.yticks(fontsize=18, color='red')
    plt.ylabel('Sentiment', fontsize=24, color='red')
    plt.tick_params(axis='both', direction='out', length=4, width=1, colors='red', grid_color='red', grid_alpha=0.5)
    plt.tight_layout()
    plt.show()

# Main function
def main():
    # Get sentiment frame
    sentiment_frame = get_ct_sentiment_frame()
    print()
    print(sentiment_frame)
    # Create figure
    make_fig(sentiment_frame)

# Entry point of the program
if __name__ == '__main__':
    main()
