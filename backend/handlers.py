from models import *
from services import *
from flask import make_response, jsonify


def handle_query(query):
    query_req, err = query_decoder(query)
    if err != '':
        return None, err
    print(query_req.msg_type, query_req.search_phrase, query_req.cnt)
    err = validate_query(query_req)
    if err != '':
        return None, err
    result, err = query_solr(query_req)
    if err != '':
        return None, err

    return make_response(
        jsonify({"result": result}),
        200
    ), ""


def handle_query_with_date(query):
    query_with_date_req, err = query_with_date_decoder(query)
    if err != '':
        return None, err
    print(query_with_date_req.msg_type, query_with_date_req.search_phrase,
          query_with_date_req.cnt, query_with_date_req.start_date, query_with_date_req.end_date)
    err = validate_query_with_date(query_with_date_req)
    if err != '':
        return None, err
    result, err = query_with_date_solr(query_with_date_req)
    if err != '':
        return None, err
    return make_response(
        jsonify({"result": result}),
        200
    ), ""


def handle_crawl(crawl):
    crawl_req, err = crawl_decoder(crawl)
    if err != '':
        return None, err
    err = validate_crawl(crawl_req)
    if err != '':
        return None, err
    result, err = crawl_tweets(crawl_req)
    if err != '':
        return None, err

    return make_response(
        jsonify({"result": result}),
        200
    ), ""


def handle_summary(summary):
    summary_req, err = summary_decoder(summary)
    if err != '':
        return None, err
    err = validate_summary(summary_req)
    if err != '':
        return None, err
    result, err = get_summary(summary_req)
    if err != '':
        return None, err
    return make_response(
        jsonify({"result": result}),
        200
    ), ""
