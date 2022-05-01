# import libraries
from turtle import position
import numpy as np 
import pandas as pd
import requests

import xlsxwriter
import math

from scipy import stats
from statistics import mean
from pprint import pprint

# import API token
from secrets import IEX_CLOUD_API_TOKEN

# import utilities module
import utils

# -------------------------------------------------------------------------------

def portfolio_input():
    ''' Function to accpet input value of your portfolio'''

    # Global variable to access across files
    global portfolio_size
    # Enter the portfolio size
    portfolio_size = input("Enter the value of your porfolio : \n")

    # Exception handling for value errors
    try:
        val = float(portfolio_size)
    except ValueError:
        print("Invalid input! \n Please try again")
        portfolio_size = input("Enter the value of your porfolio")



# -------------------------------------------------------------------------------
def callAPI(stocks):
    ''' Call from IMEX API the '''

    # Creating column Headers for the HQM DataFrame
    # The parameters include ticker, price, number of shares, 
    # Price rturns - one year, six months, three months, one month
    # Return percentiles - one year, six months, three months, one month
    hqm_columns = [
                'Ticker', 
                'Price', 
                'Number of Shares to Buy', 
                'One-Year Price Return', 
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score'
                ]

    # Create the HQM data frame with the new columns
    hqm_dataframe = pd.DataFrame(columns= hqm_columns)

    # Creating groups of 100 symbols within the symbol set
    symbol_groups = list(utils.chunks(stocks['Ticker'], 100))
    
    # List to store symbol groups in the form of stings
    symbol_strings = []

    # Converting list of lists into a comma separated string of lists
    for i in range(len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))

    
    for symbol_string in symbol_strings:
        # The URL for the batch api call in f string format
        batch_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
        
        # Make a batch API Call and store the information in a data variable 
        # Convert it to json format from requests format
        data = requests.get(batch_url).json()
        # pprint(data)

        # Append the batch data to individul columns of the row
        for symbol in symbol_string.split(','):
            hqm_dataframe = hqm_dataframe.append(
                pd.Series([
                        symbol, 
                        data[symbol]['quote']['latestPrice'], 
                        'N/A', 
                        data[symbol]['stats']['year1ChangePercent'], 
                        'N/A',
                        data[symbol]['stats']['month6ChangePercent'],
                        'N/A',
                        data[symbol]['stats']['month3ChangePercent'],
                        'N/A',
                        data[symbol]['stats']['month1ChangePercent'],
                        'N/A',
                        'N/A'
                        ],
                        index = hqm_columns),
            ignore_index= True           
            )

    return hqm_dataframe


# -------------------------------------------------------------------------------
def calulatePercentiles(hqm_dataframe):
    '''To identify high-quality momentum, 
    we're going to build a strategy that selects stocks from 
    the highest percentiles of: 
    * 1-month price returns
    * 3-month price returns
    * 6-month price returns
    * 1-year price returns
    Using the scipy stats module
    '''
    pd.DataFrame(hqm_dataframe)
    # Using a list to loop through the time periods
    time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]
    # Calculte momentum percentiles for each time period 
    for row in hqm_dataframe.index:
        for time_period in time_periods:
            hqm_dataframe.loc[row, f'{time_period} Return Percentile'] = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100

    return hqm_dataframe
# -------------------------------------------------------------------------------
def calculateHQMScore(hqm_dataframe):
    ''' The `HQM Score` will be the arithmetic mean of the 4 momentum 
    percentile scores that we calculated'''
    pd.DataFrame(hqm_dataframe)
      # Using a list to loop through the time periods
    time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

    for row in hqm_dataframe.index:
        # Store a list of momentum percentiles to use for the calculation of averages
        momentum_percentiles = []
        
        for time_period in time_periods:
            # Append the percentiles of different time periods to the momumtum_percentiles list
            momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'], )
        
        # Calculate the mean of the momentum percentiles
        hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)

    return hqm_dataframe

def selectTopStocks(n,hqm_dataframe):
    '''
    Select the best stocks based on the number of stocks you want 
    to invest in
    '''
    # Sort the hqm_dataframe in  descending order to get the best performing stocks 
    hqm_dataframe.sort_values(by = 'HQM Score', ascending = False, inplace = True)
    # Select the n nest stocks
    hqm_dataframe = hqm_dataframe[:int(n)+1]

    return hqm_dataframe

# -------------------------------------------------------------------------------
def calculateShares(hqm_dataframe):
    ''' Function to calculate total number of shares'''

    hqm_dataframe = hqm_dataframe.reset_index()
    # Find the postition size for the equally weighted portfolio strategy
    position_size = float(portfolio_size)/len(hqm_dataframe.index)

    # Calculate the number of shares to buy
    for i in range (len(hqm_dataframe['Ticker'])-1):
        hqm_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/hqm_dataframe['Price'][i])

    return hqm_dataframe

# -------------------------------------------------------------------------------
def executeStrategy(hqm_dataframe):
    ''' Generate results based on the strategy '''

    utils.savetoExcel(hqm_dataframe)


