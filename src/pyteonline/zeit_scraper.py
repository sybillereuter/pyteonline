import html
import requests
import json
from bs4 import BeautifulSoup
from .zeit_article import Article
from .summarizer_t5 import T5Summarizer
from .logging_config import setup_logging


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
        articles_list = []
        response = self.get_webpage()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article')
        for article in articles[:20]:
            data_zplus = article.get('data-zplus', None)  # no Zeit+ articles, we want the content
            if data_zplus is None or data_zplus != 'zplus':
                article_obj = self.extract_info(article)
                if (article_obj is not None
                        and article_obj.teaser_text is not None
                        and article_obj.summary is not None):
                    articles_list.append(article_obj)
        return articles_list

    def extract_info(self, article):
        article_link = self.get_link(article)
        article_title = self.get_title(article)
        img_link = self.get_image(article)
        teaser_text = self.get_teaser(article)
        summary = self.generate_summary(article_link)
        return Article(article_link, article_title, img_link, teaser_text, summary)

    @staticmethod
    def get_link(article):
        link = article.find('a')
        if link is not None:
            article_link = link.get('href', '')
            return article_link

    @staticmethod
    def get_title(article):
        link = article.find('a')
        if link is not None:
            article_title = html.unescape(link.get_text(strip=True))
            return article_title

    @staticmethod
    def get_image(article):
        img_container = article.find('picture')
        if img_container is not None:
            img = img_container.find('img')
            if img is not None:
                return img['src']
        else:
            img = article.find('img')
            if img is not None:
                return img['src']

    @staticmethod
    def get_teaser(article):
        teaser_text_element = article.find('p')
        if teaser_text_element:
            return teaser_text_element.get_text(strip=True)

    def generate_summary(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        json_scripts = soup.find_all('script', {'type': 'application/ld+json'})
        for script in json_scripts:
            data = json.loads(script.string)
            if 'articleBody' in data:
                article_body = html.unescape(data['articleBody'])
                return self.summarizer.summarize(article_body)


if __name__ == "__main__":
    scraper = ZeitScraper()
    news = scraper.scrape_articles()

    for news_article in news:
        news_article.display_info()
