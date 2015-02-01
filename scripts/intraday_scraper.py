# -*- coding: utf-8 -*- 
from bs4 import BeautifulSoup
import requests
import sys
import re

# ----------------------------------------
# Script to scrape and process NASDAQ intraday data.
# ----------------------------------------
# Note: Unicode is enabled in this script.
# ----------------------------------------

ticker = str(sys.argv[1])

# Initial loop over the thirteen time slots in a day of trading.
for i in xrange(1, 14):

	# While loop that terminates when the full list of trades has been retrieved.
	page = 1

	while True:
		
		# Edited recently to count downwards from the highest time bracket to get the TSV in the right order.
		url = "http://www.nasdaq.com/symbol/" + str(ticker) + "/time-sales?time=" + str(14-i) + "&pageno=" + str(page)
		r = requests.get(url)

		# Process the HTML to prepare for data extraction.
		soup = BeautifulSoup(r.text)
		table = soup.find_all(id='AfterHoursPagingContents_Table')
		if not table[0]:
			print url
			quit()
		table = table[0]
		data = table.find_all('td')
		total_points = len(data)

		# Break when we hit an empty webpage.
		if total_points is 0:
			break

		# Asses how many rows of data there are.
		total_rows = int(total_points/3)

		# Extract the data we need.
		for j in xrange(0, total_rows-1):
			step = j*3
			tick = data[step].text
			price = data[step+1].text
			volume = data[step+2].text

			# Clean and process the data.
			print tick.strip() + '\t' + price.replace(u' ', '').replace('$', '') + '\t' + volume.strip().replace(',', '')

		# Advance to the next iteration.
		page += 1

