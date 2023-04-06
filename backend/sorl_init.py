import pysolr
import pandas as pd


def initSolr():
    solr = pysolr.Solr(
        'http://localhost:8983/solr/stock_project_core', always_commit=True)
    solr.ping()
    solr.delete(q='*:*')

    csv_path = "IR_New_Testing_Data - Tesing_Data.csv"
    csv_data = pd.read_csv(
        csv_path, dtype={'tweet_id': 'int64'}, float_precision='round_trip')
    csv_data['tweet_id'] = csv_data['tweet_id'].astype(str)
    extracted_data = []
    for index, row in csv_data.iterrows():
        extracted_data.append({
            "id": row["tweet_id"],
            "company": row["ticker_symbol"],
            "post_date": row["post_date"],
            "author": row["writer"],
            "raw_text": row["body"],
            "like_num": row["like_num"],
            "subjectivity": row["subjectivity"],
            "sentiment": int(row["sentiment"]),
            "clean_text": row["clean_text_no_stem_user"],
        })
    # ticker_symbol_to_name_mapping = {"AAPL": "apple",
    #                                  "AMZN": "amazon",
    #                                  "GOOGL": "google",
    #                                  "MSFT": "Microsoft",
    #                                  "TSLA": "Tesla"}

    # for i in range(len(extracted_data)):
    #     extracted_data[i]["company"] = ticker_symbol_to_name_mapping[extracted_data[i]["company"]]
    resp = solr.add(extracted_data)
    print(resp)
