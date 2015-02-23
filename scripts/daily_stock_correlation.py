import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import statsmodels.formula.api as sm
from sklearn.linear_model import LinearRegression
import scipy, scipy.stats
import datetime
import time
import Quandl
import sys

# Some stuff to get the right range of data.
seed = time.strftime("%Y-%m-%d")
finish = datetime.datetime.strptime(seed, '%Y-%m-%d')
start = finish - datetime.timedelta(days=int(sys.argv[3]))

# Boilerplate args and setup for Quandl interaction.
token = "GnTpdtBqSqCaKSZeZVd5"
first_ticker = str(sys.argv[1])
second_ticker = str(sys.argv[2])

# Retrieve the stock information from Quandl.
prefix = 'GOOG/NASDAQ_'
stock_one = Quandl.get(prefix + first_ticker, authtoken=token, trim_start=start,trim_end=finish)
stock_two = Quandl.get(prefix + second_ticker, authtoken=token, trim_start=start,trim_end=finish)

# Prepare to do the math and do the math.
prices_one = stock_one['Close']
prices_two = stock_two['Close']
covariance = prices_one.cov(prices_two)
one_stddev = prices_one.std()
two_stddev = prices_two.std()

# Print everything out.
print 'Trading days used: ' + str(len(stock_one))
correlation_coefficient = covariance/(one_stddev*two_stddev)
print correlation_coefficient
