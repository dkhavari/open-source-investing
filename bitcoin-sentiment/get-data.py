from libraries.alchemy.alchemyapi import AlchemyAPI
import requests
import datetime
import pymongo
from pymongo import MongoClient
import pipeline


# --------------------------------------------------
# Connect with the remote Mongo and prepare NLP API.
# --------------------------------------------------
client = MongoClient('ds047571.mongolab.com:47571')
db = client.coinage
db.authenticate('bit', 'coin')
collection = db['articles']
api = AlchemyAPI()

# Call the pipeline to get the Feedly articles.
articles = pipeline.get_articles()

# Iterate through and score each article, storing the important metrics in MongoDB.
for article in articles:
	date = datetime.datetime.strptime(str(article[0]), '%a %Y-%m-%d %H:%M:%S')
	url = article[1]
	engagement = float(article[2])

	text = article[3]
	title = article[4]
	text_score = float(api.sentiment("text", text)['docSentiment']['score'])
	title_received = api.sentiment("text", title)
	title_score = 0.0

	if 'score' in title_received['docSentiment']:
		title_score = float(title_received['docSentiment']['score'])

	article_entry = {'date': date, 'url': url, 'engagement': engagement, 'title_score': title_score,'text_score': text_score}
	collection.save(article_entry)
