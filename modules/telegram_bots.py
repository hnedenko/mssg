import telegram
from telegram import Bot


class TelegramBots:

    def __init__(self, telegram_bot_positivity_token, telegram_bot_negativity_token, chat_id):
        self.bot_positivity = Bot(token=telegram_bot_positivity_token)
        self.bot_negativity = Bot(token=telegram_bot_negativity_token)
        self.chat_id = chat_id

    async def send_post_to_positivity_bot(self, article):

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
            await self.bot_positivity.send_message(
                chat_id=self.chat_id,
                text=escaped_text,
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
            )
            print(f"✅ The post successfully published in Positivity Telegram {self.chat_id}.")
            return True
        except telegram.error.TelegramError as e:
            print(f"❌ Error publishing post: {e}")
            return False

    async def send_post_to_negativity_bot(self, article):

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
            await self.bot_negativity.send_message(
                chat_id=self.chat_id,
                text=escaped_text,
                parse_mode=telegram.constants.ParseMode.MARKDOWN_V2
            )
            print(f"✅ The post successfully published in Negativity Telegram {self.chat_id}.")
            return True
        except telegram.error.TelegramError as e:
            print(f"❌ Error publishing post: {e}")
            return False