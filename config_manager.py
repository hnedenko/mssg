import os
from dotenv import load_dotenv

class ConfigManager:

    def __init__(self):

        load_dotenv(dotenv_path='.venv/.env')

        self.news_sites_for_searching = ['https://gorod.dp.ua/export/rss.php']

        self.positive_threshold = 0.2
        self.negative_threshold = 0.1
        self.similarity_threshold = 0.5

        self.is_post_to_positive_channel = False
        self.is_post_to_negative_channel = False
        self.is_post_to_comfyui_channel = True

        load_dotenv(dotenv_path='.venv/.env')
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.telegram_bot_positivity_token = os.getenv("TELEGRAM_BOT_POSITIVITY_TOKEN")
        self.telegram_bot_negativity_token = os.getenv("TELEGRAM_BOT_NEGATIVITY_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def deploy(self):
        os.system('pip install -r requirements.txt')
