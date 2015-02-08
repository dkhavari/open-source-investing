#!/usr/bin/python

import sys
import os

# Take in the arguments and open the ticker file.
target_script = str(sys.argv[1])
filename = str(sys.argv[2])
f = open(filename, 'r')

# Call the script with the appropriate filename etc.
for line in f:
	ticker = str(line).strip('\n')
	os.system('python ' + target_script + ' ' + ticker + ' > ' + ticker + '-2-6-2015.tsv')