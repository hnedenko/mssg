from config_manager import ConfigManager
from modules.RSS_parser import RSSParser


if __name__ == '__main__':

    # init config and deploy app
    config_manager = ConfigManager()
    config_manager.deploy()

    # init RSS parser and parse all news from sites in config
    RSS_parser = RSSParser(config_manager.news_sites_for_searching)
    rss_articles = RSS_parser.parse_all_sites()

    for i in rss_articles:
        print(i)
