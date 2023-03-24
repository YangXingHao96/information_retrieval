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
