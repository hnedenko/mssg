import requests
from bs4 import BeautifulSoup
from readability import Document


class HTMLScraper:

    def __init__(self):
        pass

    def fetch_texts_for_articles(self, articles):
        for article in articles:
            article.set_origin_text(self.fetch_text_from_url(article.link))

    def fetch_text_from_url(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            article_text = self.extract_text_from_soup(soup)

            return article_text

        except requests.exceptions.RequestException as e:
            print(f"Load URL error {url}: {e}")
            return None
        except Exception as e:
            print(f"Parsing error {url}: {e}")
            return None

    def extract_text_from_soup(self, soup):

        doc = Document(str(soup))
        readable_html = doc.summary()
        clean_soup = BeautifulSoup(readable_html, 'html.parser')

        return clean_soup.get_text(separator=' ', strip=True)
