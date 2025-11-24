import telegram
from telegram import Bot


class TelegramBot:

    def __init__(self, telegram_bot_token, chat_id):
        self.bot = Bot(token=telegram_bot_token)
        self.chat_id = chat_id

    async def send_post(self, article):


        escaped_text = article.rewrite_text
        escaped_text = escaped_text.replace('!', r'\!')
        escaped_text = escaped_text.replace('.', r'\.')
        escaped_text = escaped_text.replace('(', r'\(')
        escaped_text = escaped_text.replace(')', r'\)')
        escaped_text = escaped_text.replace('[', r'\[')
        escaped_text = escaped_text.replace(']', r'\]')
        escaped_text = escaped_text.replace('{', r'\{')
        escaped_text = escaped_text.replace('}', r'\}')
        escaped_text = escaped_text.replace('+', r'\+')
        escaped_text = escaped_text.replace('-', r'\-')
        escaped_text = escaped_text.replace('=', r'\=')
        escaped_text = escaped_text.replace('|', r'\|')

        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=escaped_text,
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
            )
            print(f"✅ The post successfully published in Telegram {self.chat_id}.")
            return True
        except telegram.error.TelegramError as e:
            print(f"❌ Error publishing post: {e}")
            return False