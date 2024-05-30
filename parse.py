import feedparser


def parse_rss_feed(url):
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries:
        news_items.append(
            {'title': entry.title, 'link': entry.link, 'published': entry.published})
    return news_items


def get_new_news(news_items, news_cache):
    new_news = []
    for item in news_items:
        if item['link'] not in news_cache:
            new_news.append(item)
    return new_news
