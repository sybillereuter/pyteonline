class Article:

    def __init__(self, link, title, img_link, teaser_text, summary):
        self.link = link
        self.title = title
        self.img_link = img_link
        self.teaser_text = teaser_text
        self.summary = summary

    def display_info(self):
        print("Link:", self.link)
        print("Titel:", self.title)
        print("Bild-Link:", self.img_link)
        print("Teaser-Text:", self.teaser_text)
        print("Automatische Zusammenfassung", self.summary)
        print("\n" + "-"*50 + "\n")
