import html
import requests
from bs4 import BeautifulSoup
from typing import List, Optional, Dict, Any

from .article import Article
from .scraper import Scraper


class TagesschauScraper(Scraper):

    def __init__(self):
        super().__init__()
        self.api_url = "https://www.tagesschau.de/api2u/homepage/"
        self.headers = {
            "User-Agent": "PyteOnline",
            "Accept": "application/json"
        }

    def scrape_articles(self) -> List[Article]:
        try:
            articles_data = self.fetch_articles()
            return [
                article_obj for article in articles_data[:15]
                if (article_obj := self.extract_info(article))
                   and article_obj.teaser_text
                   and article_obj.summary
            ]
        except Exception as e:
            self.logger.error(f"Scraping failed: {str(e)}")
            return []

    def fetch_articles(self) -> List[Dict[str, Any]]:
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json().get("news", [])
        except Exception as e:
            self.logger.error(f"API request failed: {str(e)}")
            return []

    def extract_info(self, article_data: Dict[str, Any]) -> Optional[Article]:
        try:
            article_url = (
                    article_data.get("shareURL") or
                    article_data.get("detailsweb")
            )
            if not article_url or "/newsticker/" in article_url or "/wetter/" in article_url:
                return None

            title = html.unescape(article_data.get("title", ""))
            img_link = self.get_best_image(article_data)
            teaser = self.get_teaser(article_data)

            full_text = self.extract_full_text(article_data)
            summary = self.summarizer.summarize(full_text) if full_text else ""

            return Article(article_url, title, img_link, teaser, summary)
        except Exception as e:
            self.logger.warning(f"Failed to process article: {str(e)}")
            return None

    @staticmethod
    def extract_full_text(article_data: Dict[str, Any]) -> str:
        content_parts = []

        for content in article_data.get("content", []):
            try:
                content_type = content.get("type")
                content_value = content.get("value", "")

                if not content_value:
                    continue

                if content_type == "text":
                    try:
                        soup = BeautifulSoup(content_value, "html.parser")
                        text = soup.get_text(" ", strip=True)
                        content_parts.append(text)
                    except Exception as e:
                        text = " ".join(content_value.split())
                        content_parts.append(text)

                elif content_type == "headline":
                    headline = content_value.replace("<h2>", "").replace("</h2>", "").strip()
                    content_parts.append(f"\n{headline}\n")

            except Exception as e:
                continue

        full_text = "\n".join(content_parts)
        full_text = "\n".join(line.strip() for line in full_text.splitlines() if line.strip())

        return full_text

    @staticmethod
    def get_best_image(article_data: Dict[str, Any]) -> Optional[str]:
        image_variants = (
                article_data.get("teaserImage", {}).get("imageVariants", {}) or
                article_data.get("firstFrame", {}).get("imageVariants", {})
        )

        # TODO get copyright info to display..?
        for variant in ["16x9-1280", "16x9-960", "16x9-640"]:
            if variant in image_variants:
                return image_variants[variant]

        return None

    @staticmethod
    def get_teaser(article_data: Dict[str, Any]) -> str:
        for content in article_data.get("content", []):
            if content.get("type") == "text":
                text = content.get("value", "")
                if "<strong>" in text:
                    strong_start = text.find("<strong>") + len("<strong>")
                    strong_end = text.find("</strong>", strong_start)
                    if strong_end > strong_start:
                        teaser = text[strong_start:strong_end]
                        return html.unescape(teaser.strip())

        for content in article_data.get("content", []):
            if content.get("type") == "text":
                text = content.get("value", "")
                if text.strip():
                    text = BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
                    return html.unescape(text.split(".")[0] + ".")

        return html.unescape(
            article_data.get("firstSentence", "") or ""
        ).strip()


if __name__ == "__main__":
    scraper = TagesschauScraper()
    news = scraper.scrape_articles()

    for news_article in news:
        news_article.display_info()

