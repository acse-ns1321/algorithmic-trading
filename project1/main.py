
# import libraries
import numpy as np
import pandas as pd
import requests
import math
import utils
# libraray to write python files to excel
import xlsxwriter

# import API token
from secrets import IEX_CLOUD_API_TOKEN

# -------------------------------------------------------------------------------------------------------------------------------------

# create data frame
def createData(fname):
    ''' Add atock price and market capitilazitaion to pandas dataframe '''

    # read csv file containing tickers
    stocks = pd.read_csv(fname)

    # column headers for final output file
    column_headers = ['Ticker', 'Price','Market Capitalization', 'Number Of Shares to Buy']

    # data frame for final output file
    output_dataframe = pd.DataFrame(columns = column_headers)
    return stocks, column_headers, output_dataframe
# -------------------------------------------------------------------------------------------------------------------------------------

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# -------------------------------------------------------------------------------------------------------------------------------------

# create the api call
def callAPI(stocks, col_heads , output_dataframe, base_url, end_point):
    ''' Create batch requests for API calls to improve optimization.
     IEX Cloud limits their batch API calls to 100 tickers per request '''
    ...

    # split tickers into groups of 100
    symbol_groups = list(chunks(stocks['Ticker'], 100))

    # Create a comma separated list of symbol groups
    symbol_strings = []
    for i in range(len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))

    # Call API in batches
    for symbol_string in symbol_strings:

        # Create a batch API call
        batch_api_call_url = base_url+end_point+f'={symbol_string}&token={IEX_CLOUD_API_TOKEN}'

        # Get requests from API and save as json data
        data = requests.get(batch_api_call_url).json()
        

        for symbol in symbol_string.split(','):
            # print(data[symbol == 'HFC']['quote']['latestPrice'])
            # data -> symbol -> quote -> " VARIABLE"
            try:
              output_dataframe = output_dataframe.append(
                                            pd.Series([symbol, 
                                                    data[symbol]['quote']['latestPrice'], 
                                                    data[symbol]['quote']['marketCap'], 
                                                    'N/A'], 
                                                    index = col_heads), 
                                            ignore_index = True)
            except KeyError:
                continue
            
    return output_dataframe

# -------------------------------------------------------------------------------------------------------------------------------------  
def calculateShares(portfolio_size, output_dataframe):
    '''Number of shares of each stock to buy'''

    # Divide amount equally among the numberr of shares(equally weighted shares)
    position_size = float(portfolio_size) / len(output_dataframe.index)

    # Calculate number of shares depending on share price
    for i in range(0, len(output_dataframe['Ticker'])-1):
        output_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size / output_dataframe['Price'][i])

    return output_dataframe

# -------------------------------------------------------------------------------------------------------------------------------------  



def main():
    ''' Main Function'''

    # File containing name of stock tickers
    fname = 'project1/sp_500_stocks.csv'

    # Create an empty output dataframe
    stocks, column_heads,output =  createData(fname)

    base_url = 'https://sandbox.iexapis.com/stable'
    end_point = '/stock/market/batch/?types=quote&symbols'

    # Add API data to created output data frame
    output = callAPI(stocks, column_heads,output, base_url, end_point)
    
    print("-------------------------------------------------------------------")
    print("                  EQUAL WEIGHT S&P 500                             ")
    print("-------------------------------------------------------------------")
    # Take portfolio size as input from the user
    portfolio_size = 0
    while True:
        portfolio_size = input("Enter the value of your portfolio:\n")
        try:
            val = float(portfolio_size)
            break
        except ValueError:
            print("This is not a number. Please enter a valid number")
            portfolio_size = input("Enter the value of your portfolio:")
            
    print("Creating Portfolio ... \n")
    # Calculate number of shares and append to data frame
    output = calculateShares(portfolio_size, output)
    
    # save to excel
    print("Portfolio Created ! \n")
    utils.savetoExcel(output)
    print("Your output is ready! Check the xlsx file generated ")
if __name__=='__main__':
    main()