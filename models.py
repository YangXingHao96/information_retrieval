class query():
    def __init__(self, message_type: str, search_phrase: str, query_cnt: int):
        self.msg_type = message_type
        self.search_phrase = search_phrase
        self.cnt = query_cnt


class crawl():
    def __init__(self, keyword: str, crawl_count: int):
        self.keyword = keyword
        self.cnt = crawl_count


def query_decoder(req):
    try:
        q = query(req['type'], req['content'], req['count'])
        return q, ""
    except Exception as e:
        return None, "An exception has occured " + str(e)


def crawl_decoder(req):
    try:
        q = crawl(req['keyword'], req['crawl_count'])
        return q, ""
    except Exception as e:
        return None, "An exception has occured " + str(e)
