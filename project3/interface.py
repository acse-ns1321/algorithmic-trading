import pandas as pd
from sklearn import metrics
# import functions from files
import value_strategy
import utils


def beginTrade():
    ''' Function that runs the interface for the trade 
    and returns output both in xlsx file and  on the terminal
    '''
    
    print("------------------------------------------------------------")
    print("---------------  VALUE STRATEGY  ---------------------------")
    print("------------------------------------------------------------")

    print(" Wecome to the Momentum Strategy Script \n")
    print(" Please enter the size of your portfolio \n")
    value_strategy.portfolio_input()
    print("------------------------------------------------------------")

    print("Importing Tickers and Testing the API Call ...\n") 
    stocks = utils.readData()
    print("------------------------------------------------------------")


    print("Calling APIs...\n")
    value_dataframe = value_strategy.callAPI(stocks)
    print("------------------------------------------------------------")

    print("Building a value strategy ...\n")
    value_dataframe,metrics = value_strategy.calulatePercentiles(value_dataframe)
    value_dataframe = value_strategy.calculateScore(value_dataframe, metrics)
    print("------------------------------------------------------------")

    # Specify the number of stocks you want to invest in
    nstocks = input("Enter the number of value stocks you want to invest in : \n")
    value_dataframe = value_strategy.selectTopStocks(nstocks, value_dataframe)
    

    print("------------------------------------------------------------")
    print("Calculting the number of shares ...\n")
    value_dataframe=  value_strategy.calculateShares(value_dataframe)
    print("------------------------------------------------------------")

    print("Executing the strategy and generating the results ...\n")
    value_strategy.executeStrategy(value_dataframe)
    print("------------------------------------------------------------")

    print("Results Generated Successfully!\n")