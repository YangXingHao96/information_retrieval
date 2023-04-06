from flask import Flask,  jsonify, request
from handlers import *
from const import *
import sorl_init
app = Flask(__name__)


@app.route('/query', methods=[HTTP_POST])
def query_sentiment():
    try:
        req = request.get_json()
        result, err = handle_query(req)
        if err:
            return jsonify(error=err), 400
        else:
            print(result)
            return result
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('/querywithdate', methods=[HTTP_POST])
def query_sentiment_with_date():
    try:
        req = request.get_json()
        result, err = handle_query_with_date(req)
        if err:
            return jsonify(error=err), 400
        else:
            print(result)
            return result
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route("/crawl", methods=[HTTP_POST])
def crawl_tweets():
    try:
        req = request.get_json()
        result, err = handle_crawl(req)
        if err:
            return jsonify(error=err), 400
        else:
            print(result)
            return result
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route("/summary", methods=[HTTP_POST])
def query_summary():
    try:
        req = request.get_json()
        result, err = handle_summary(req)
        if err:
            return jsonify(error=err), 400
        else:
            print(result)
            return result
    except Exception as e:
        return jsonify(error=str(e)), 400


if __name__ == "__main__":
    sorl_init.initSolr()
    app.run()
