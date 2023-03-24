import pysolr
solr = pysolr.Solr(
    'http://localhost:8983/solr/test_core', always_commit=True)
solr.ping()

solr.add([
    {
        "body": ["Apple (AAPL), Alphabet (GOOG), Berkshire Hathaway (BRK/A), &amp; Microsoft (MSFT) have the largest cash positions among American companies, &amp; they are garnering much higher interest income as short-term rates have risen above 4% from near zero at the start of 2022\n👇🏻1/"],
        "id":"b440f9d4-5cf6-4cbd-b973-d57960c2135f",
        "like_num":0,
        "sentiment":1,
        "ticker_symbol":"apple",
        "tweet_id":1633084793268174848,
        "post_date":"2023-03-07T12:38:50Z",
        "retweet_num":0,
        "writer":"akshay_sol",
    },
    {
        "body": ["Top 10 trending stocks on WallStreetBets as of Mar 7, 2023\n\n1. Apple $AAPL\n2. Tesla $TSLA\n3. Nvidia $NVDA\n4. Meta Platforms $META\n5. Amazon $AMZN\n6. Snap $SNAP\n7. Coinbase $COIN\n8. Walt Disney $DIS\n9. JPMorgan Chase $JPM\n10. Alphabet $GOOG"],
        "id":"5d95f233-15e1-438a-96f3-95d25c1b6a34",
        "like_num":0,
        "sentiment":1,
        "ticker_symbol":"apple",
        "tweet_id":1633082476909449216,
        "post_date":"2023-03-07T12:29:38Z",
        "retweet_num":0,
        "writer":"Marcus_US_stock",
    },
    {
        "body": ["Apple's $AAPL iPhone 13 was the best-selling smartphone of 2022\n\n8 out of the top 10 best selling smartphones around the world in 2022 were iPhones according to Counterpoint research- MacRumors https://t.co/5sJyTeVEHR"],
        "id":"a20842ab-6e95-4c09-868f-85415c8b6eb7",
        "like_num":48,
        "sentiment":1,
        "ticker_symbol":"apple",
        "tweet_id":1633079084979830784,
        "post_date":"2023-03-07T12:16:09Z",
        "retweet_num":8,
        "writer":"StockMKTNewz",
    },
    {
        "body": ["APPLE 🍎🍏 ( AAPL) \n.It started to move march 2004 with perfect cup with handle over 9 years\n. It adjusted $12 to $700.\n. Eight leaders came back to lead other market cycle after they topped. https://t.co/FkCTxwl4e8"],
        "id":"9663c1c5-11ac-4511-8c5a-d05ec787fdaf",
        "like_num":1,
        "sentiment":1,
        "ticker_symbol":"apple",
        "tweet_id":1633078248362987520,
        "post_date":"2023-03-07T12:12:50Z",
        "retweet_num":0,
        "writer":"IManghaila",
    }
])

results = solr.search('body:aapl')

# # The ``Results`` object stores total results found, by default the top
# # ten most relevant results and any additional data like
# # facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("The result is '{0}'.".format(result['body']))


# res = solr.query('SolrClient_unittest', {
#     'q': 'product_name:Lorem',
#     'facet': True,
#     'facet.field': 'facet_test',
# })
# print(res.get_results_count())
