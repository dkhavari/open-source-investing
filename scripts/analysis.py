import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import csv
import re

# Parse in the TSV file.
tsvin = open(sys.argv[1],'rb')
tsvin = csv.reader(tsvin, delimiter='\t')

# for row in tsvin:
# 	print row

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
	
times_np = np.array(times)
prices_np = np.array(prices)

plt.plot(times_np, prices_np, 'b-')
if len(sys.argv) > 2:
	plt.title(str(sys.argv[2]))

# Show the plot.
plt.show()