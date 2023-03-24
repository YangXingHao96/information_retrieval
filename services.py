from models import *
from const import *
import pysolr
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as twitter
import pandas as pd
import itertools
import uuid


def validate_query(query_req: query) -> str:
    if not isinstance(query_req.msg_type, str):
        return "query type: must be of type string"
    elif query_req.msg_type == "":
        return "query type must not be empty"
    elif query_req.search_phrase == "":
        return "query search phrase must not be empty"
    elif not isinstance(query_req.cnt, int):
        return "query count must be of type integer"
    elif query_req.cnt <= 0:
        return "query count must not be less than or equals to zero"
    print("validation successful")
    return ""


def validate_crawl(crawl_req: crawl) -> str:
    if not isinstance(crawl_req.cnt, int):
        return "crawl count must be an integer"
    elif crawl_req.cnt <= 0:
        return "crawl count must be greater than 0"
    elif not isinstance(crawl_req.keyword, str):
        return "crawl keyword must be of type string"
    elif crawl_req.keyword == "":
        return "crawl keyword must not be empty"
    print("validation successful")
    return ""


def query_solr(query_req: query):
    try:
        sorl = pysolr.Solr(SOLR_URL, always_commit=True)
        query_phrase = ""
        if query_req.msg_type == "":
            query_phrase = '*:' + query_req.search_phrase
        else:
            query_phrase = query_req.msg_type + ':' + query_req.search_phrase
        print(query_phrase)
        result = sorl.search(query_phrase, rows=query_req.cnt)
        final = []
        for res in result:
            final.append(res)

        return final, ""
    except Exception as e:
        return None, "Exception: " + str(e.with_traceback())


def crawl_tweets(crawl_req: crawl) -> list[list[str], str]:
    try:
        sent_analyser = SentimentIntensityAnalyzer()
        tweets = twitter.TwitterSearchScraper(crawl_req.keyword).get_items()
        sliced_scraped_tweets = itertools.islice(tweets, crawl_req.cnt)
        solr = pysolr.Solr(
            SOLR_URL, always_commit=True)
        tweets_to_add = []
        res = []
        for tweet in sliced_scraped_tweets:
            sentiment = 0
            if sent_analyser.polarity_scores(tweet.rawContent)["compound"] >= 0:
                sentiment = 1
            else:
                sentiment = 0
            temp = {
                "body": [tweet.rawContent],
                "id": str(uuid.uuid4()),
                "like_num": tweet.likeCount,
                "sentiment": sentiment,
                "ticker_symbol": crawl_req.keyword,
                "tweet_id": tweet.id,
                "post_date": str(tweet.date),
                "retweet_num": tweet.retweetCount,
                "writer": tweet.user.username,
            }
            tweets_to_add.append(temp)
            res.append(tweet.rawContent)
        solr.add(tweets_to_add)
        return res, ""
    except Exception as e:
        return None, "Exception: " + str(e.with_traceback())
