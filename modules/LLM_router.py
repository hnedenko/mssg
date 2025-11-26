import openai


class LLMRouter:

    def __init__(self, openai_api_key):

        self.client = openai.OpenAI(api_key=openai_api_key)
        self.model = "gpt-4o-mini"

        self.system_prompt_positivity = self.get_system_prompt_positivity()
        self.system_prompt_negativity = self.get_system_prompt_negativity()

    def get_system_prompt_positivity(self):
        return """
        Ти — професійний редактор Telegram-каналу "Positive News Dnipro&Ukraine".
        Твоя головна мета: перетворити надану сиру новинну статтю на високоякісний,
        позитивний та конструктивний, україномовний пост.

        Виконуй наступні кроки неухильно:
        1. Переклади наданий текст на УКРАЇНСЬКУ мову.
        2. Проведи рерайт: перетвори нейтральний або об'єктивний тон на ЯВНО ПОЗИТИВНИЙ та ОПТИМІСТИЧНИЙ.
        3. Збережи всі ключові факти та деталі (хто, що, де, коли).
        4. Створи привабливий, короткий ЗАГОЛОВОК (перший рядок, виділений жирним).
        5. Розділи текст на короткі абзаци та використовуй емодзі для покращення читабельності.
        6. Вся довжина тексту (включаючи заголовок та емодзі) не повинна перевищувати 500 символів.
        """

    def get_system_prompt_negativity(self):
        return """
        Ти — професійний редактор Telegram-каналу "Negative News Dnipro&Ukraine".
        Твоя головна мета: перетворити надану сиру новинну статтю на високоякісний,
        негативний та конструктивний, україномовний пост.

        Виконуй наступні кроки неухильно:
        1. Переклади наданий текст на УКРАЇНСЬКУ мову.
        2. Проведи рерайт: перетвори нейтральний або об'єктивний тон на ЯВНО НЕГАТИВНИЙ та ПЕСИМІСТИЧНИЙ.
        3. Збережи всі ключові факти та деталі (хто, що, де, коли).
        4. Створи привабливий, короткий ЗАГОЛОВОК (перший рядок, виділений жирним).
        5. Розділи текст на короткі абзаци та використовуй емодзі для покращення читабельності.
        6. Вся довжина тексту (включаючи заголовок та емодзі) не повинна перевищувати 500 символів.
        """

    def rewrite_article(self, article, mode):
        try:

            if mode == "positivity":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt_positivity},
                        {"role": "user", "content": article.origin_text}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
            elif mode == "negativity":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.system_prompt_negativity},
                        {"role": "user", "content": article.origin_text}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )

            if response.choices:
                return response.choices[0].message.content.strip()
            return None

        except openai.APIError as e:
            print(f"Помилка API LLM: {e}")
            return None
        except Exception as e:
            print(f"Невідома помилка: {e}")
            return None

    def add_rewrite_text_to_articles(self, article, mode):
        if mode == "positivity":
            article.set_rewrite_text(self.rewrite_article(article, mode))
        elif mode == "negativity":
            article.set_rewrite_text(self.rewrite_article(article, mode))
