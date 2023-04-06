class query():
    def __init__(self, message_type: str, search_phrase: str, query_cnt: int):
        self.msg_type = message_type
        self.search_phrase = search_phrase
        self.cnt = query_cnt


class query_with_date():
    def __init__(self, message_type: str, search_phrase: str, query_cnt: int, start_date: str, end_date: str):
        self.msg_type = message_type
        self.search_phrase = search_phrase
        self.cnt = query_cnt
        self.start_date = start_date
        self.end_date = end_date


class crawl():
    def __init__(self, company: str, crawl_count: int):
        self.cnt = crawl_count
        self.company = company


class summary():
    def __init__(self, company: str, start_date: str, end_date: str):
        self.company = company
        self.start_date = start_date
        self.end_date = end_date


def query_decoder(req):
    try:
        q = query(req['type'], req['content'], req['count'])
        return q, ""
    except Exception as e:
        return None, "An exception has occured " + str(e)


def query_with_date_decoder(req):
    try:
        q = query_with_date(req['type'], req['content'],
                            req['count'], req['start_date'], req['end_date'])
        return q, ""
    except Exception as e:
        return None, "An exception has occured " + str(e)


def crawl_decoder(req):
    try:
        q = crawl(req['company'], req['crawl_count'])
        return q, ""
    except Exception as e:
        return None, "An exception has occured " + str(e)


def summary_decoder(req):
    try:
        q = summary(req['company'], req['start_date'], req['end_date'])
        return q, ""
    except Exception as e:
        return None, "An exception has occured " + str(e)
