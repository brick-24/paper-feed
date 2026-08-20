from function.news import fetch_news

def test_news_rss_http_check():
    headlines = fetch_news(limit=1)

    assert len(headlines) == 1
    assert headlines[0].strip()
