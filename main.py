from config_manager import ConfigManager

if __name__ == '__main__':

    # init config and deploy app
    config_manager = ConfigManager()
    config_manager.deploy()

from modules.RSS_parser import RSSParser
from modules.data_manager import DataManager
from modules.HTML_scraper import HTMLScraper
from modules.positivity_analyzer import PositivityAnalyser
from modules.vectorizer import Vectorizer
from modules.LLM_router import LLMRouter
from modules.telegram_bot import TelegramBot
import asyncio


if __name__ == '__main__':

    # init RSS parser and parse all news from sites in config
    RSS_parser = RSSParser(config_manager.news_sites_for_searching)
    rss_articles = RSS_parser.parse_all_sites()

    # init app modules
    data_manager = DataManager()
    HTML_scraper = HTMLScraper()
    vectorizer = Vectorizer()
    positivity_analyzer = PositivityAnalyser()
    llm_router = LLMRouter(config_manager.openai_api_key)
    telegram_bot = TelegramBot(config_manager.telegram_bot_token, config_manager.telegram_chat_id)

    # app loop for each article from RSS feed
    for article in rss_articles:

        # check ID uniqueness in DB to next steps
        is_article_id_unique = data_manager.is_article_id_unique_in_main(article)
        if is_article_id_unique:

            # Fetch all article texts from HTML
            HTML_scraper.fetch_texts_for_articles([article])

            # Article semantic vectorization
            vectorizer.add_vector_to_articles([article])

            # Add new article to DB
            data_manager.add_article_in_main(article)

            # check only "positivity" and "semantics_unique" to publication to "Positive News Dnipro&Ukraine" Telegram channel
            is_article_positivity = positivity_analyzer.is_article_positivity(article, config_manager.positive_threshold)
            is_article_semantics_unique = data_manager.is_article_semantics_unique_in_positivity_articles(article, config_manager.similarity_threshold)
            if is_article_positivity and is_article_semantics_unique:

                # API LLM call to translation and rewrite article
                llm_router.add_rewrite_text_to_articles(article)
                # article.set_rewrite_text(article.origin_text)

                # public article to "Positive News Dnipro&Ukraine" Telegram channel
                asyncio.run(telegram_bot.send_post(article))

                # Add new article to "positivity_articles" collection
                data_manager.add_article_in_positivity_articles(article)

