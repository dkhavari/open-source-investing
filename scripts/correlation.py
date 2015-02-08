from tsvprocessing import tsv_to_tuple_list
from pandas import Series
import datetime as dt
import time
import sys
import csv
import re

# ------------------------------
# Function: Grouping and Averaging
# ------------------------------
def make_grouped_second_prices(equity, top_bound, bottom_bound, decrement):
	# Create result vector and variables.
	averaged_time_groups = []
	equity_counter = 0
	# Iterate through the time vector in ten-second steps.
	for i in xrange(0, 2340):
		# Iterate through the equity and group based on ten-second intervals.
		sum_of_interval = 0.0
		number_to_average = 0.0 # Currently testing with this.
		while True:
			# Make sure we avoid any indexing errors.
			if equity_counter >= len(equity):
				break
			# Set up the trade and execution time for use.
			trade = equity[equity_counter]
			time_of_execution = trade[0]
			# If the time of execution is in the proper range, use it.
			if time_of_execution <= top_bound and time_of_execution > bottom_bound:
				price = trade[1]
				sum_of_interval += price
				number_to_average += 1
				equity_counter += 1
			else:
				break

		# Get the important metric: 10-second interval average price.
		if sum_of_interval is 0.0: # In other words, nothing found in range.
				average_executed_price = averaged_time_groups[i-1]
		else:
			average_executed_price = sum_of_interval / number_to_average
		averaged_time_groups.append(average_executed_price)
		# Move the loop forward.
		top_bound = top_bound - decrement
		bottom_bound = top_bound - decrement
	return averaged_time_groups

# Access the two equity files passed in.
equity_one = str(sys.argv[1])
equity_two = str(sys.argv[2])
file_one = open(equity_one, 'r')
file_two = open(equity_two, 'r')
# Parse the TSV files into something intelligible.
tsv_one = csv.reader(file_one, delimiter='\t')
tsv_two = csv.reader(file_two, delimiter='\t')

# Use the miniature tsvprocessing module I made.
equity_one = tsv_to_tuple_list(tsv_one)
equity_two = tsv_to_tuple_list(tsv_two)

# Set up the loop for aggregating to 10-second averages.
decrement = dt.timedelta(seconds = 10)
top_bound = dt.datetime.strptime('16:00:00', '%H:%M:%S')
bottom_bound = top_bound - decrement

# Get the averages.
equity_one_ten_sec_avg = make_grouped_second_prices(equity_one, top_bound, bottom_bound, decrement)
equity_two_ten_sec_avg = make_grouped_second_prices(equity_two, top_bound, bottom_bound, decrement)

# Create the pandas series.
one = Series(equity_one_ten_sec_avg)
two = Series(equity_two_ten_sec_avg)

# Compute Covariance.
covariance = one.cov(two)

# Compute standard deviations.
one_stddev = one.std()
two_stddev = two.std()

# Correlation coefficient...
correlation_coefficient = covariance/(one_stddev*two_stddev)

print correlation_coefficient




















