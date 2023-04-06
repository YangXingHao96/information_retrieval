

def build_search_request(query_types, query_terms, start_date, end_date, total_cnt):
    keymapping = {
        "content": "raw_text",
        "author": "author",
        "company": "company"
    }
    if not start_date:
        return {
            "type": keymapping[query_types],
            "content": query_terms,
            "count": int(total_cnt)
        }
    return {
        "type": keymapping[query_types],
        "content": query_terms,
        "count": int(total_cnt),
        "start_date": start_date,
        "end_date": end_date
    }


def build_index_request(company_name, count):
    return {
        "crawl_count": int(count),
        "company": company_name
    }
