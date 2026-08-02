# a function to generate the output seen in the file pfizerResearch.py
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
import numpy as np


## note to self for when you return to this code ##

# widened data is data centred around the announcement date 


def event_window(ticker, announcementDate):

    announcementDate = pd.to_datetime(announcementDate)

    startDate = announcementDate - timedelta(days=14)
    endDate = announcementDate + timedelta(days=14) # look either side of the announcement date by a couple of weeks, ten trading days 

    widened_data = yf.download(ticker, startDate, endDate, auto_adjust=True)

    # compute the percentage change between consecutive close prices 
    widened_data['Return'] = widened_data['Close'].pct_change() 
    widened_data['Cumulative Return'] = (1 + widened_data['Return']).cumprod() - 1 
    
    announcement_idx = widened_data.index.get_indexer([announcementDate], method='nearest')[0]
    baseline_idx = max(announcement_idx - 1, 0)
    baseline = widened_data['Cumulative Return'].iloc[baseline_idx]
    widened_data['Cumulative Return'] = widened_data['Cumulative Return'] - baseline

    
    widened_data['      Trading Days Relative'] = np.arange(len(widened_data)) - announcement_idx
    # create an array of values from 0 to the length of widened data
    # subtract the index of the announcement date from each so that the announcement date is centered at zero

plot_data = widened_data.dropna()  # drop all rows with NaN values (the first row has no return value)
    plt.plot(plot_data.index, plot_data['Cumulative Return'] * 100)
    plt.title(ticker)
    plt.axvline(x=pd.Timestamp(announcementDate), color='red', linestyle='--', label='Announcement Day') # plot a vertical line at the date where the announcement was made 
    plt.ylabel("Percentage change")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.legend()
    plt.grid(True)
    # plt.show()
    ##

    return widened_data

def big_change(ticker, rangeStartDate, rangeEndDate): # use this function to look over a large range of dates and find the largest drop dates. see if this is consistent with what i expect 

    full_data = yf.download(ticker, rangeStartDate, rangeEndDate, auto_adjust=True)
    # find the percentage return between adjacent closing prices 



    full_data['Returns'] = full_data['Close'].pct_change()
    full_data['Returns'] = full_data['Returns'].clip(lower=-0.9, upper=0.9) # clipping the returns to avoid outliers, for example stock splits

positive_change = full_data['Returns'].nlargest(10) * 100
negative_change = full_data['Returns'].nsmallest(10) * 100

table_of_data = pd.DataFrame({
    "Positive (%)": positive_change,
    "Negative (%)": negative_change
})



return table_of_data

