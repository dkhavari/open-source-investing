import math

# Global constants.
SENTINEL_VALUE = -1000.0

def compute_moving_averages(articles, coll, delta):

	# Get the newest and oldest articles.
	newest = articles[0]['date']
	oldest = articles[articles.count() - 1]['date']
	time_period = newest - oldest

	slices = int(math.ceil(time_period.total_seconds() / delta.total_seconds()))

	sentiment_values_clean = []
	sentiment_values_all = []

	# Compute the average for each of the buckets.
	for i in xrange(0, slices):
		current_upper = newest - i*delta
		current_lower = newest - (i + 1)*delta

		# Make the query every time.
		articles_in_period = coll.find({'date': {'$gt': current_lower, '$lte': current_upper}})

		total = 0.0
		count_of_articles = float(articles_in_period.count())

		# Skip if there are no articles.
		if count_of_articles == 0:
			sentiment_values_all.append(SENTINEL_VALUE) # Place a sentinel value.
			continue

		for news_article in articles_in_period:
			total += news_article['text_score']

		total /= count_of_articles

		sentiment_values_clean.append(total)
		sentiment_values_all.append(total)

	return (sentiment_values_clean, sentiment_values_all)
