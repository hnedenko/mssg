import os

class ConfigManager:

    def __init__(self):
        self.news_sites_for_searching = ['http://www.prodnepr.dp.ua/rss/news_all.xml',
                                         'https://com1.org.ua/feed/']

    def deploy(self):
        os.system('pip install -r requirements.txt')
