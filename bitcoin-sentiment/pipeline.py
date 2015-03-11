from libraries import feedlyclient
import requests
from bs4 import BeautifulSoup
import cfscrape
import datetime
from pymongo import MongoClient
import pymongo


def get_text(url):
    scraper = cfscrape.create_scraper() #this is necessary to bypass CloudFlare doing its job
    
    html = scraper.get(url, verify=False).content #scrapes html. take that, CloudFlare
    soup = BeautifulSoup(html)
    for script in soup(["script", "style"]):  #removes all js and unnecessary links, might put back links, though.
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines()) # breaks multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # drops blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def get_articles():
    client = MongoClient('ds047571.mongolab.com:47571')
    db = client.coinage
    db.authenticate('bit', 'coin')
    collection = db['articles']
    
    new_articles = []
    
    # Boilerplate Feedly interaction.
    user_id = 'da75f8c1-616c-4f00-8a45-79e77cb2e99e'
    token = 'AmVJitV7ImEiOiJGZWVkbHkgRGV2ZWxvcGVyIiwiZSI6MTQzMTkyMzQyNzM4NywiaSI6ImRhNzVmOGMxLTYxNmMtNGYwMC04YTQ1LTc5ZTc3Y2IyZTk5ZSIsInAiOjYsInQiOjEsInYiOiJwcm9kdWN0aW9uIiwidyI6IjIwMTUuOCIsIngiOiJzdGFuZGFyZCJ9:feedlydev'
    feedly = feedlyclient.FeedlyClient(sandbox=False) # Instantiate my client.
    user_subs = feedly.get_user_subscriptions(token) # Gets all of my subscriptions.


    for sub in user_subs:
        sub_id = sub['id'] # Gets the id of each successive subscription.
        content = feedly.get_feed_content(access_token = token, streamId = sub_id, unreadOnly = False, newerThan = False)
        articles = content['items'] # Finds the articles in the content dict.
        for article in articles:
            title = article['title']
            list_ = article['alternate'] # Pulls the article metadata like url.
            if 'engagementRate' not in str(article):
                continue
            engagement_rate =  article['engagementRate']
            dict_ = list_[0] # Random nesting: for whatever reason the previous line returned a list of length one containing a dict.
            url = dict_['href'] # This is where the url is stored.
            if collection.find_one({'url': url}) == None:
                unixy_time = article['published'] # Returns when it was published in 13-digit unix-like timestamp.
                time_and_date = datetime.datetime.fromtimestamp(int(unixy_time/1000)).strftime('%a %Y-%m-%d %H:%M:%S') #convert from their weird unix-esque 13-digit time format.
                text = get_text(url)
                article_info = (time_and_date, url, engagement_rate, text, title)
                new_articles.append(article_info)
    return new_articles
