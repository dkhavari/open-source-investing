import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame, Series
import sys
import csv
import re

# Parse in the TSV file.
tsvin = open(sys.argv[1],'rb')
tsvin = csv.reader(tsvin, delimiter='\t')

# Build up price, time data arrays
times = []
prices = []

for row in tsvin:

	# I actually need to convert these into datetime objects.
	time = row[0]
	price = row[1]

	# Fix up the dates.
	date_object = datetime.strptime(time, '%H:%M:%S')

	# Append to the lists, which will be converted into numpy arrays.
	prices.append(float(re.sub("[a-zA-Z]", "", price)))
	times.append(date_object)
	
# Get a price array so we can get some information.
prices = Series(prices)
mean = Series.mean(prices)
stddev = Series.std(prices)
median = Series.median(prices)

# Print out all of the analyzed data.
print str(sys.argv[1])
print 'Mean: ' + str(mean)
print 'Median: ' + str(median)
print 'Standard Deviation: ' + str(stddev)
print 'Trades Used: ' + str(len(prices))