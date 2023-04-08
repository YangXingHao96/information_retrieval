from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import requests
import json
import utils

app = Flask(__name__)
app.secret_key = 'mysecretkey'
search_url = "http://127.0.0.1:5000/query"
search_withdate_url = "http://127.0.0.1:5000/querywithdate"
crawl_url = "http://127.0.0.1:5000/crawl"
summary_url = "http://127.0.0.1:5000/summary"


@app.route('/')
def display():
    return render_template('display.html')


@app.route('/index', methods=['POST'])
def index_submit():
    # retrieve the form data
    company_name = request.form['company name']
    count = request.form['count']
    index_req = utils.build_index_request(company_name, count)
    req_headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(crawl_url, data=json.dumps(
        index_req), headers=req_headers)
    data = response.json()
    if response.status_code != 200:
        print(
            f"{response.status_code} error: Post request to {crawl_url} could not be completed.")
        print(f"Error returned: {data['error']}")
        return render_template('display.html')
    tweets = []
    for raw_tweet in data["result"]:
        processed_tweet = {
            'content': raw_tweet["raw_text"][0],
            'author': raw_tweet["author"],
            'posted_date': raw_tweet["post_date"],
            'subjectivity': int(raw_tweet["subjectivity"]),
            'sentiment': int(raw_tweet["sentiment"])
        }
        tweets.append(processed_tweet)
    # do something with the form data (e.g., store it in a database)
    # ...

    # redirect to a success page
    return render_template('index.html', tweets=tweets)


@app.route('/search', methods=['POST'])
def search():
    query_type = request.form['query_type']
    query_terms = request.form['query_terms']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    total_cnt = request.form['total_cnt']
    search_req = utils.build_search_request(
        query_type, query_terms, start_date, end_date, total_cnt)
    req_headers = {
        'Content-Type': 'application/json'
    }
    print(search_req)
    # make HTTP call to backend server with the user's input
    if not start_date:
        response = requests.post(search_url, data=json.dumps(
            search_req), headers=req_headers)
    else:
        response = requests.post(search_withdate_url, data=json.dumps(
            search_req), headers=req_headers)
    data = response.json()
    if response.status_code != 200:
        print(
            f"{response.status_code} error: Post request to {search_url} could not be completed.")
        print(f"Error returned: {data['error']}")
        return render_template('display.html')
    data = response.json()
    tweets = []
    for raw_tweet in data["result"]:
        processed_tweet = {
            'content': raw_tweet["raw_text"][0],
            'author': raw_tweet["author"][0],
            'posted_date': raw_tweet["post_date"],
            'subjectivity': int(raw_tweet["subjectivity"][0]),
            'sentiment': int(raw_tweet["sentiment"][0])
        }
        tweets.append(processed_tweet)
    suggestions = data["corrections"]
    return render_template('results.html', tweets=tweets, suggestions=suggestions)


@app.route('/summary', methods=['POST'])
def summary():
    company = request.form['company']
    start_date = request.form['start_date_summary']
    end_date = request.form['end_date_summary']
    summary_req = utils.build_summary_request(company, start_date, end_date)
    req_headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(summary_url, data=json.dumps(
        summary_req), headers=req_headers)
    data = response.json()
    if response.status_code != 200:
        print(
            f"{response.status_code} error: Post request to {summary_req} could not be completed.")
        print(f"Error returned: {data['error']}")
        return render_template('display.html')
    print(data["result"])
    return render_template("piecharts.html", result=data["result"])


if __name__ == '__main__':
    app.run(port=5001)
