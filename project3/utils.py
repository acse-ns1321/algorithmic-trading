import pandas as pd
import xlsxwriter
import requests

# import the token for API access
from secrets import IEX_CLOUD_API_TOKEN

# -------------------------------------------------------------------------------------------------------------------------------------  
def readData():
    ''' Function to read tickers from a CSV File into a dataFrame
     and test the API call 
    '''
    # Import sock tickers from csv file into pandas dataframe
    fname = 'project3/sp_500_stocks.csv'
    stocks = pd.read_csv(fname)

    # Testing the API Call
    symbol = 'AAPL'
    api_url = f'https://sandbox.iexapis.com/stable/stock/{symbol}/quote?token={IEX_CLOUD_API_TOKEN}'
    status_code = requests.get(api_url).status_code

    # Check the status of the API call
    if status_code == 200:
        print('API Calling works!\n')
    else:
        print('API Calling failed! \n Send a report to the developer')
    return stocks
# -------------------------------------------------------------------------------------------------------------------------------------  
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
# -------------------------------------------------------------------------------------------------------------------------------------  
def savetoExcel(output):
    ''' Function that saves pandas output to excel'''

    # Initialize Xlsx Writer Object
    writer = pd.ExcelWriter('project3/Value_Strategy.xlsx', engine='xlsxwriter')

    # Convert to Excel
    output_dataframe = pd.DataFrame(output)
    output_dataframe.to_excel(writer, sheet_name='Value Strategy', index = False)

    # Creating the formats we need fot the Excel file
    background_color = '#E6E6FA'
    font_color = '#2222AA'

    string_template = writer.book.add_format(
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

    dollar_template = writer.book.add_format(
            {
                'num_format':'$0.00',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )

    integer_template = writer.book.add_format(
            {
                'num_format':'0',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )

    float_template = writer.book.add_format(
            {
                'num_format':'0',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )

    percent_template = writer.book.add_format(
            {
                'num_format':'0.0%',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )
    column_formats = {
                        'A': ['Ticker', string_template],
                        'B': ['Price', dollar_template],
                        'C': ['Number of Shares to Buy', integer_template],
                        'D': ['Price-to-Earnings Ratio', float_template],
                        'E': ['PE Percentile', percent_template],
                        'F': ['Price-to-Book Ratio', float_template],
                        'G': ['PB Percentile',percent_template],
                        'H': ['Price-to-Sales Ratio', float_template],
                        'I': ['PS Percentile', percent_template],
                        'J': ['EV/EBITDA', float_template],
                        'K': ['EV/EBITDA Percentile', percent_template],
                        'L': ['EV/GP', float_template],
                        'M': ['EV/GP Percentile', percent_template],
                        'N': ['RV Score', percent_template]
                    }

    for column in column_formats.keys():
        writer.sheets['Value Strategy'].set_column(f'{column}:{column}', 25, column_formats[column][1])
        writer.sheets['Value Strategy'].write(f'{column}1', column_formats[column][0], column_formats[column][1])

    writer.save() 
# -------------------------------------------------------------------------------------------------------------------------------------  