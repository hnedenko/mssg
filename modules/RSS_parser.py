import feedparser

from article import Article


class RSSParser:

    def __init__(self, news_sites_for_searching):
        self.news_sites_for_searching = news_sites_for_searching

    def parse_all_sites(self):
        rss_articles = list()
        for site in self.news_sites_for_searching:
            rss_articles.extend(self.parse_site(site))
        return rss_articles

    def parse_site(self, site):
        entries = feedparser.parse(site).entries
        articles = list()

        for entrie in entries:
            articles.append(Article(entrie['title'], entrie['link'], entrie['published']))

        return articles
