import xlrd as xl
import numpy
import sys


# Helper functions
def median(lst):
    return numpy.median(numpy.array(lst))

def avg(lst):
	return numpy.mean(numpy.array(lst))

# Bring in the list of tickers to analyze.
ticker_list = str(sys.argv[1])
f = open(ticker_list, 'r')

# Iterate and populate the correlation vector.
correlations = []
movements = []

# Now start testing some hypotheses...
for line in f:

	# Get the worksheet we want from xlrd.
	directory_name = line[:line.index(' ')]
	workbook = xl.open_workbook('commodities_intraday/' + str(directory_name) + '/' + str(line.strip('\n')))
	worksheet = workbook.sheets()[0]

	# Retrieve the relevant prices.
	opening_price = float(str(worksheet.row(1)[1])[7:])
	one_hour_in = float(str(worksheet.row(61)[1])[7:])
	closing_price = float(str(worksheet.row(391)[1])[7:])
	movement_in_first_hour = one_hour_in - opening_price
	movement_one_hour_to_close = closing_price - one_hour_in

	# Just to see how many of the correlations are positive.
	movement_compared_to_first_hour = 100.0*(movement_one_hour_to_close / movement_in_first_hour)
	correlations.append(movement_compared_to_first_hour)

	# Get the interesting returns data here.
	movements.append((one_hour_in, movement_one_hour_to_close))


# Figure out the percentage for which it's a positive correlation.
positive_corr = 0.0
total = 0.0
for result in correlations:
	if float(result) > 0.0:
		positive_corr += 1.0
	total += 1.0

# OUTPUT 1: Percentage for which correlation is positive.
print "Positive Correlation Percentage: " + str(100*positive_corr/total) + "%"
print ""

movements_following_correlation = []
neg_correlated = []

# Now for all positive correlations, print out what the return was.
for i in xrange(0, len(movements)):
	purchase_price = movements[i][0]
	price_movement = movements[i][1]
	correlation = correlations[i]

	# If we have a positive correlation...
	if correlation > 0.0:
		absolute_percentage_change = abs(100*price_movement/purchase_price)
		movements_following_correlation.append(absolute_percentage_change)
	else:
		absolute_percentage_change = abs(100*price_movement/purchase_price)
		neg_correlated.append(absolute_percentage_change)

# OUTPUT #2: Average movements for positively and negatively correlated movements from +1hr to close.

print "Average Price Movement Following Correlation: " + str(avg(movements_following_correlation)) + "%"
print "Median Price Movement Following Correlation: " + str(median(movements_following_correlation)) + "%"

print ""

print "Average Price Movement Not Following Correlation: " + str(avg(neg_correlated)) + "%"
print "Median Price Movement Not Following Correlation: " + str(median(neg_correlated)) + "%"

