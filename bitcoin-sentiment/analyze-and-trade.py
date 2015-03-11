import datetime
from datetime import timedelta as td
import pymongo as pymongo
from pymongo import MongoClient
from movingavg import compute_moving_averages
import math
import sys


# Constants.
MAX_ARTICLES = 250
WINDOW_SIZE = 3 # hours

# --------------------------------------------------
# Connect with the remote Mongo and prepare NLP API.
# --------------------------------------------------
client = MongoClient('ds047571.mongolab.com:47571')
db = client.coinage
db.authenticate('bit', 'coin')
collection = db['articles']

# Get a healthy number of articles to ensure we have enough.
articles = collection.find().sort("date",pymongo.DESCENDING).limit(MAX_ARTICLES)

# Get the current time.
current_time = datetime.datetime.now()

# --------------------------------------------------
# Call a function to get the average sentiment for
# time periods of any specified size / time delta.
# --------------------------------------------------
time_delta = td(hours=float(sys.argv[1]))
results = compute_moving_averages(articles, collection, time_delta)

# --------------------------------------------------
# Time to work with the Bollinger Bands.
# --------------------------------------------------