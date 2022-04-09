import pandas as pd
import xlsxwriter


def readCSV():
    ''' Function to read CSV File into a dataFrame'''

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def savetoExcel(output):
    ''' Function that saves pandas output to excel'''

    # Initialize Xlsx Writer Object
    writer = pd.ExcelWriter('project1/recommended_trades.xlsx', engine='xlsxwriter')

    # Convert to Excel
    output_dataframe = pd.DataFrame(output)
    output_dataframe.to_excel(writer, sheet_name='Recommended Trades', index = False)

    # Creating the formats we need fot the Excel file
    background_color = '#E6E6FA'
    font_color = '#2222AA'

    string_format = writer.book.add_format(
            {
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )

    dollar_format = writer.book.add_format(
            {
                'num_format':'$0.00',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )

    integer_format = writer.book.add_format(
            {
                'num_format':'0',
                'font_color': font_color,
                'bg_color': background_color,
                'border': 1
            }
        )
    column_formats = { 
                    'A': ['Ticker', string_format],
                    'B': ['Price', dollar_format],
                    'C': ['Market Capitalization', dollar_format],
                    'D': ['Number of Shares to Buy', integer_format]
                    }

    for column in column_formats.keys():
        writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 20, column_formats[column][1])
        writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], string_format)

    writer.save() 
# -------------------------------------------------------------------------------------------------------------------------------------  