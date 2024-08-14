import time
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_caching import Cache
from .logging_config import setup_logging
from .zeit_scraper import ZeitScraper


logger = setup_logging('pyteonline.log', 'pyteonline-logger')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
scraper = ZeitScraper()
news = []


class SchedulerManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._scheduler = BackgroundScheduler()
            cls._instance._scheduler.add_job(
                cls._instance._scrape_and_clear,
                'interval',
                hours=1,
                id='scrape_job'
            )
            cls._instance._scheduler.start()
            logger.info("Scheduler started with interval of 1 hour.")
        return cls._instance

    def _scrape_and_clear(self):
        start_time = time.time()
        global news
        news = scraper.scrape_articles()
        logger.info("Scraping done!")
        if news:
            cache.clear()
            logger.info("Cleared cache!")
        execution_time = time.time() - start_time
        logger.info(f"Execution time of _scrape_and_clear: {execution_time} seconds")

    def get_news(self):
        if not news:
            self._scrape_and_clear()
        return news

    def stop_scheduler(self):
        if self._scheduler:
            self._scheduler.shutdown()
            logger.info("Scheduler stopped.")


scheduler_manager = SchedulerManager()


@app.route('/')
def index():
    current_news = scheduler_manager.get_news()
    return render_template('pyte_online.html', news=current_news)


if __name__ == '__main__':
    app.run(debug=False)
