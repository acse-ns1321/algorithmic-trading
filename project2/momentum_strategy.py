# import libraries
import numpy as np 
import pandas as pd
import requests

import xlsxwriter
import math

from scipy import stats

# import API token
from secrets import IEX_CLOUD_API_TOKEN

# import utilities module
import utils

# -------------------------------------------------------------------------------

def portfolio_input():
    ''' Function to accpet input value of your portfolio'''

# -------------------------------------------------------------------------------
def callAPI():
    ''' Call from IMEX API the '''


# -------------------------------------------------------------------------------
def createMomentumDatabase():
    ''' '''

# -------------------------------------------------------------------------------
def calulatePercentiles():
    '''To identify high-quality momentum, 
    we're going to build a strategy that selects stocks from 
    the highest percentiles of: 
    * 1-month price returns
    * 3-month price returns
    * 6-month price returns
    * 1-year price returns
    '''
# -------------------------------------------------------------------------------
def calculateHQMScore():
    ''' The `HQM Score` will be the arithmetic mean of the 4 momentum 
    percentile scores that we calculated'''


def selectTopStocks():
    '''
    Select the best stocks based on the number of stocks you want 
    to invest in
    '''

# -------------------------------------------------------------------------------
def calculateShares():
    ''' Function to calculate total number of shares'''


# -------------------------------------------------------------------------------
def executeStrategy():
    ''' Generate results based on the strategy '''
    

