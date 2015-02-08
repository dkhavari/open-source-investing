from datetime import datetime
import re

def tsv_to_tuple_list(tsv):
	tuple_list = []
	for row in tsv:
		# Get these into useful forms.
		date_object = datetime.strptime(row[0], '%H:%M:%S')
		price_string = str(row[1])
		volume_float = float(row[2])
		
		# Create tuple and append.
		trade_entry = (date_object, float(re.sub("[a-zA-Z]", "", price_string)), volume_float)
		tuple_list.append(trade_entry)
	return tuple_list