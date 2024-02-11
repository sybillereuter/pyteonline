from flask import Flask, render_template
from .zeit_scraper import ZeitScraper

app = Flask(__name__)
# todo advanced python scheduler!
scraper = ZeitScraper()
news = scraper.scrape_articles()


@app.route('/')
def index():
    return render_template('pyte_online.html', news=news)


if __name__ == '__main__':
    app.run(debug=True)
