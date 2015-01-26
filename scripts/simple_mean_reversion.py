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
start = finish - datetime.timedelta(days=150)

# Boilerplate args and Quandl interaction.
token = "GnTpdtBqSqCaKSZeZVd5"
filename = sys.argv[1]

# Get the ticker file.
f = open(filename, 'r')

# Create the stock list.
list_of_stocks = []

# Loop through everything...
for line in f:

	ticker = line.strip('\n')
	source = 'GOOG/NASDAQ_' + ticker

	# Receive the data that I want.
	try:
		past_150d = Quandl.get(source, authtoken=token, trim_start=start,trim_end=finish)
	except:
		continue

	# Figure out how to manipulate it a little bit.
	closing_prices = past_150d['Close']

	# Get useful metrics for computation.
	mean = Series.mean(closing_prices)
	stddev = Series.std(closing_prices)
	try:
		current_price = closing_prices[len(closing_prices) - 1]
	except:
		continue

	# Decide if this is a stock worth looking at.
	if current_price < (mean - stddev):

		# Some testing stuff.
		print '<><><> ' + str(ticker) + ' <><><>'

		# Compute by how much the current price is under the mean.
		stddevs_under_mean = (mean - current_price)/stddev		
		stock_entry = [ticker, stddevs_under_mean]
		list_of_stocks.append(stock_entry)

# Sort the tickers by the one farthest beneath the mean, then print in that order.
sorted_stocks = sorted(list_of_stocks, key=lambda x: float(x[1]), reverse=True)

for entry in sorted_stocks:
	print str(entry[0]) + ' -' + str(entry[1])
