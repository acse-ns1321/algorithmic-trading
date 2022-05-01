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
    
    # columns for the dataframe
    value_columns = ['Ticker',
    'Price',
    'Number of Shares to Buy', 
    'Price-to-Earnings Ratio',
    'PE Percentile',
    'Price-to-Book Ratio',
    'PB Percentile',
    'Price-to-Sales Ratio',
    'PS Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'EV/GP',
    'EV/GP Percentile',
    'RV Score'
]



    # Create the value strategy data frame with the new columns
    value_dataframe = pd.DataFrame(columns= value_columns)

      # Creating groups of 100 symbols within the symbol set
    symbol_groups = list(utils.chunks(stocks['Ticker'], 100))
    
    # List to store symbol groups in the form of stings
    symbol_strings = []

    # Converting list of lists into a comma separated string of lists
    for i in range(len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))

    
    for symbol_string in symbol_strings[:1]:
        # The URL for the batch api call in f string format
        batch_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
        
        # Make a batch API Call and store the information in a data variable 
        # Convert it to json format from requests format
        data = requests.get(batch_url).json()
        # pprint(data)


        # Append the batch data to individul columns of the row
        for symbol in symbol_string.split(','):
             
            # P/E Ratio
            pe_ratio = data[symbol]['quote']['peRatio']

            # P/B Ratio
            pb_ratio = data[symbol]['advanced-stats']['priceToBook']

            #P/S Ratio
            ps_ratio = data[symbol]['advanced-stats']['priceToSales']

            # EV/EBITDA
            enterprise_value = data[symbol]['advanced-stats']['enterpriseValue']
            ebitda = data[symbol]['advanced-stats']['EBITDA']
            ev_to_ebitda = enterprise_value/ebitda

            # EV/GP
            gross_profit = data[symbol]['advanced-stats']['grossProfit']
            ev_to_gross_profit = enterprise_value/gross_profit


            value_dataframe = value_dataframe.append(
                pd.Series([
                         symbol,
                data[symbol]['quote']['latestPrice'],
                'N/A',
                data[symbol]['quote']['peRatio'],
                'N/A',
                data[symbol]['advanced-stats']['priceToBook'],
                'N/A',
                data[symbol]['advanced-stats']['priceToSales'],
                'N/A',
                ev_to_ebitda,
                'N/A',
                ev_to_gross_profit,
                'N/A',
                'N/A'
                        ],
                        index = value_columns),
            ignore_index= True           
            )

    return value_dataframe


# -------------------------------------------------------------------------------
def calulatePercentiles(value_dataframe):
    '''To identify high-quality momentum, 
    we're going to build a strategy that selects stocks from 
    the highest percentiles 
    Using the scipy stats module
    '''
    pd.DataFrame(value_dataframe)
    metrics = {
            'Price-to-Earnings Ratio': 'PE Percentile',
            'Price-to-Book Ratio':'PB Percentile',
            'Price-to-Sales Ratio': 'PS Percentile',
            'EV/EBITDA':'EV/EBITDA Percentile',
            'EV/GP':'EV/GP Percentile'
    }

    for row in value_dataframe.index:
        for metric in metrics.keys():
            value_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(value_dataframe[metric], value_dataframe.loc[row, metric])/100

    # # Print each percentile score to make sure it was calculated properly
    # for metric in metrics.values():
    #     print(value_dataframe[metric])

    #Return the entire DataFrame    
    return value_dataframe, metrics
# -------------------------------------------------------------------------------
def calculateScore(value_dataframe, metrics):
    ''' The `HQM Score` will be the arithmetic mean of the 4 momentum 
    percentile scores that we calculated'''
    pd.DataFrame(value_dataframe)
    for row in value_dataframe.index:
        value_percentiles = []
        for metric in metrics.keys():
            value_percentiles.append(value_dataframe.loc[row, metrics[metric]])
        value_dataframe.loc[row, 'RV Score'] = mean(value_percentiles)
    
    return value_dataframe

#--------------------------------------------------------------------------------------------- 

def selectTopStocks(n,value_dataframe):
    '''
    Select the best stocks based on the number of stocks you want 
    to invest in and remove the glamour stocks
    '''
    # Sort the value_dataframe in  descending order to get the best performing stocks 
    value_dataframe.sort_values('Price-to-Earnings Ratio', inplace = True)

    # Remove glamour stocks
    value_dataframe = value_dataframe[value_dataframe['Price-to-Earnings Ratio'] > 0]

    # Select the n best stocks
    value_dataframe = value_dataframe[:int(n)+1]

    return value_dataframe


# -------------------------------------------------------------------------------
def calculateShares(value_dataframe):
    ''' Function to calculate total number of shares'''

    value_dataframe = value_dataframe.reset_index()
    # Find the postition size for the equally weighted portfolio strategy
    position_size = float(portfolio_size)/len(value_dataframe.index)

    # Calculate the number of shares to buy
    for i in range (len(value_dataframe['Ticker'])-1):
        value_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/value_dataframe['Price'][i])

    return value_dataframe

# -------------------------------------------------------------------------------
def executeStrategy(value_dataframe):
    ''' Generate results based on the strategy '''

    utils.savetoExcel(value_dataframe)

