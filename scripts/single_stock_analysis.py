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

# Arguments: ticker days

# Some stuff to get the right range of data.
seed = time.strftime("%Y-%m-%d")
finish = datetime.datetime.strptime(seed, '%Y-%m-%d')
start = finish - datetime.timedelta(days=int(sys.argv[2]))

print str(start)
print str(finish)

# Boilerplate args and Quandl interaction.
token = "GnTpdtBqSqCaKSZeZVd5"
ticker = str(sys.argv[1])

# Get the specific ticker and analyze it, printing the results.
source = 'GOOG/NASDAQ_' + ticker
information = Quandl.get(source, authtoken=token, trim_start=start,trim_end=finish)

# Get the prices we need to calculate beta etc.
closing_prices = information['Close']
mean = Series.mean(closing_prices)
stddev = Series.std(closing_prices)
median = Series.median(closing_prices)

# Print out everything I need.
print ticker
print 'Mean: ' + str(mean)
print 'Median: ' + str(median)
print 'Standard Deviation: ' + str(stddev)
print 'Trading days used: ' + str(len(information))