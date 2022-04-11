import pandas as pd
# import functions from files
import momentum_strategy
import utils


def beginTrade():
    ''' Function that runs the interface for the trade 
    and returns output both in xlsx file and  on the terminal
    '''

    print("------------------------------------------------------------")
    print("---------------MOMENTUM STRATEGY----------------------------")
    print("------------------------------------------------------------")

    print(" Wecome to the Momentum Strategy Script \n")
    print(" Please enter the size of your portfolio \n")
    momentum_strategy.portfolio_input()
    print("------------------------------------------------------------")

    print("Importing Tickers and Testing the API Call ...\n") 
    stocks = utils.readData()
    print("------------------------------------------------------------")


    print("Calling APIs...\n")
    hqm_dataframe = momentum_strategy.callAPI(stocks)
    print("------------------------------------------------------------")

    print("Building a high quality momentum strategy ...\n")
    hqm_dataframe = momentum_strategy.calulatePercentiles(hqm_dataframe)
    hqm_dataframe = momentum_strategy.calculateHQMScore(hqm_dataframe)
    print("------------------------------------------------------------")

    # Specify the number of stocks you want to invest in
    nstocks = input("Enter the number of HQM stocks you want to invest in : \n")
    hqm_dataframe = momentum_strategy.selectTopStocks(nstocks, hqm_dataframe)

    print("Calculting the number of shares ...\n")
    hqm_dataframe=  momentum_strategy.calculateShares(hqm_dataframe)
    print("------------------------------------------------------------")

    print("Executing the strategy and generating the results ...\n")
    momentum_strategy.executeStrategy(hqm_dataframe)
    print("------------------------------------------------------------")

    print("Results Generated Successfully!\n")




