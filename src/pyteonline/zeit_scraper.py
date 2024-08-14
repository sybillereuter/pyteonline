import html
import json
import requests
from bs4 import BeautifulSoup
from .logging_config import setup_logging
from .summarizer_t5 import T5Summarizer
from .zeit_article import Article


class ZeitScraper:

    def __init__(self):
        self.url = 'https://www.zeit.de/index'
        self.summarizer = T5Summarizer()
        self.logger = setup_logging('pyteonline.log', 'pyteonline-logger')

    def get_webpage(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response
        else:
            self.logger.error(f"Error fetching site. Status code: {response.status_code}")
            raise Exception(f"Error fetching site. Status code: {response.status_code}")

    def scrape_articles(self):
        response = self.get_webpage()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')

        return [
            article_obj
            for article in articles[:20]
            if article.get('data-zplus') != 'zplus'
            and (article_obj := self.extract_info(article))
            and article_obj.teaser_text
            and article_obj.summary
        ]

    def extract_info(self, article):
        article_link = self.get_link(article)
        article_title = self.get_title(article)
        img_link = self.get_image(article)
        teaser_text = self.get_teaser(article)
        summary = self.generate_summary(article_link)
        return Article(article_link, article_title, img_link, teaser_text, summary)

    @staticmethod
    def get_link(article):
        return article.find('a').get('href', '') if article.find('a') else ''

    @staticmethod
    def get_title(article):
        return html.unescape(article.find('a').get_text(strip=True)) if article.find('a') else ''

    @staticmethod
    def get_image(article):
        img = article.find('picture img') or article.find('img')
        return img['src'] if img else None

    @staticmethod
    def get_teaser(article):
        return article.find('p').get_text(strip=True) if article.find('p') else None

    def generate_summary(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        json_scripts = soup.find_all('script', {'type': 'application/ld+json'})

        for script in json_scripts:
            if data := json.loads(script.string):
                if article_body := data.get('articleBody'):
                    return self.summarizer.summarize(html.unescape(article_body))


if __name__ == "__main__":
    scraper = ZeitScraper()
    news = scraper.scrape_articles()

    for news_article in news:
        news_article.display_info()
