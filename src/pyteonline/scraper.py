import html
import json

from bs4 import BeautifulSoup
import requests

from .logging_config import setup_logging
from .summarizer_t5 import T5Summarizer


class Scraper:

    def __init__(self):
        self.summarizer = T5Summarizer()
        self.logger = setup_logging('pyteonline.log', 'pyteonline-logger')

    def scrape_articles(self):
        raise NotImplementedError("Subclasses must implement this method")

    def extract_info(self, article_data):
        raise NotImplementedError("Subclasses must implement this method")

    def generate_summary(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        json_scripts = soup.find_all('script', {'type': 'application/ld+json'})

        for script in json_scripts:
            if data := json.loads(script.string):
                if article_body := data.get('articleBody'):
                    return self.summarizer.summarize(html.unescape(article_body))
        return None
