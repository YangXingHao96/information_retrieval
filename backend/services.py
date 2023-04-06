import datetime
from models import *
from const import *
import pysolr
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as twitter
import pandas as pd
import itertools
from clean import *
import uuid


def validate_query(query_req: query):
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


def validate_query_with_date(query_req: query_with_date):
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
    elif query_req.start_date == "":
        return "query start date must not be empty"
    elif query_req.end_date == "":
        return "query end date must not be empty"
    elif query_req.start_date >= query_req.end_date:
        return "query end date must be greater than query start date"
    print("validation successful")
    return ""


def validate_crawl(crawl_req: crawl):
    if not isinstance(crawl_req.cnt, int):
        return "crawl request count must be an integer"
    elif crawl_req.cnt <= 0:
        return "crawl request count must be greater than 0"
    elif not isinstance(crawl_req.company, str):
        return "crawl request company name must be of type string"
    elif crawl_req.company == "":
        return "crawl request company name must not be empty"
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


def query_with_date_solr(query_req: query_with_date):
    try:
        sorl = pysolr.Solr(SOLR_URL, always_commit=True)
        start_yr, start_mth, start_day = query_req.start_date.split("-")
        end_yr, end_mth, end_day = query_req.end_date.split("-")
        start_yr, start_mth, start_day = int(
            start_yr), int(start_mth), int(start_day)
        end_yr, end_mth, end_day = int(end_yr), int(end_mth), int(end_day)
        start_date = datetime.datetime(start_yr, start_mth, start_day)
        end_date = datetime.datetime(end_yr, end_mth, end_day)
        start_date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_date_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        range_query = 'post_date:[{} TO {}]'.format(
            start_date_str, end_date_str)
        params = {
            'q': query_req.msg_type + ':' + query_req.search_phrase,
            'fq': range_query,
            'rows': query_req.cnt,
            'sort': 'post_date desc'
        }
        results = sorl.search(**params)
        final = []
        for res in results:
            final.append(res)
        return final, ""
    except Exception as e:
        return None, "Exception: " + str(e.with_traceback())


def crawl_tweets(crawl_req: crawl):
    prep = SubPreprocessor()
    sent_analyser = SentimentIntensityAnalyzer()
    tweets = twitter.TwitterSearchScraper(crawl_req.company).get_items()
    print(tweets)
    sliced_scraped_tweets = itertools.islice(tweets, crawl_req.cnt)
    solr = pysolr.Solr(
        SOLR_URL, always_commit=True)
    df = pd.DataFrame(columns=['id', 'company', 'post_date', 'author',
                               'raw_text', 'like_num', 'subjectivity', 'sentiment'])
    for tweet in sliced_scraped_tweets:
        print(tweet)
        sentiment = 0
        if sent_analyser.polarity_scores(tweet.rawContent)["compound"] >= 0:
            sentiment = 1
        else:
            sentiment = 0
        temp = {
            "id": tweet.id,
            "company": crawl_req.company,
            "post_date": str(tweet.date),
            "author": tweet.user.username,
            "raw_text": [tweet.rawContent],
            "like_num": tweet.likeCount,
            "subjectivity": 0,
            "sentiment": sentiment
        }
        print(temp)
        df = pd.concat(
            [df, pd.DataFrame([temp], columns=df.columns)], ignore_index=True)
    print("performing transformation")
    df = prep.transform(df)
    extracted_data = []
    for index, row in df.iterrows():
        extracted_data.append({
            "id": row["id"],
            "company": row["company"],
            "post_date": row["post_date"],
            "author": row["author"],
            "raw_text": row["raw_text"],
            "like_num": row["like_num"],
            "subjectivity": row["subjectivity"],
            "sentiment": row["sentiment"],
            "clean_text": row["clean_text"],
        })

    solr.add(extracted_data)
    return extracted_data, ""
    # except Exception as e:
    #     return None, "Exception: " + str(e.with_traceback())
