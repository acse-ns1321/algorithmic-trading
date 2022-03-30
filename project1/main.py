
# import libraries
import numpy as np
import pandas as pd
import requests
import math

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
    final_output = pd.DataFrame(columns = column_headers)

    # for symbol in stocks['Ticker']:
    #     # base url + endpoint that contains marketcap and price
    #     api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}'

    #     # get request from the url in the form of json data and store in data
    #     data = requests.get(api_url).json()

    #     # Append to final data frame 
    #     # Values in order :
    #     # Symbol (ticker) read from out csv file
    #     # Price - the latestPrice in json data
    #     # Market Cap - the marketCap variable in the json data
    #     # Number Of Shares to Buy - to be caluclated so set it to N/A
    #     final_output = final_output.append(pd.Series([symbol, 
    #                                                 data['latestPrice'], 
    #                                                 data['marketCap'], 
    #                                                 'N/A'], 
    #                                                 index = column_headers), 
    #                                         ignore_index = True)

    return stocks, column_headers, final_output

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

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
                # print("Stock ",symbol," not available")
                continue
            
    return output_dataframe.head
    
def calculateShares():
    ...


def main():
    ''' Main Function'''

    fname = 'project1/sp_500_stocks.csv'

    stocks, column_heads,output =  createData(fname)

    base_url = 'https://sandbox.iexapis.com/stable'
    end_point = '/stock/market/batch/?types=quote&symbols'

    output_api = callAPI(stocks, column_heads,output, base_url, end_point)
    print(output_api)




if __name__=='__main__':
    main()