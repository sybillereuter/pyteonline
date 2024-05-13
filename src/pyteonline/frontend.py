from flask import Flask, render_template
from .zeit_scraper import ZeitScraper
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
scraper = ZeitScraper()
news = []


def scrape():
    global news
    news = scraper.scrape_articles()


@app.route('/')
def index():
    return render_template('pyte_online.html', news=news)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape, 'interval', hours=1)
    scheduler.start()

    scrape()

    app.run(debug=True)
