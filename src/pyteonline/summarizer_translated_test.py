import unittest
from .summarizer_translated import TranslationSummarizer


class TestTranslationSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = TranslationSummarizer()

    def test_summarize_text(self):
        text = """
        "Rechtsextreme haben sich aufgemacht, dieses Land zu spalten", 
        sagte SPD-Chef Lars Klingbeil am Sonntag in der ARD – alle seien 
        in der Verantwortung dagegenzuhalten. "Ich wünsche mir vor allem, 
        dass sie aufstehen, dass sie laut sind", sagte Klingbeil. 
        Nach den Correctiv-Enthüllungen dürfe niemand mehr schweigen. 
        Im Gegenteil müssten "diejenigen, die gerade ruhig sind, auch 
        laut die Stimme erheben und sagen: Wir lassen nicht zu, 
        dass dieses Land so polarisiert und gespaltet wird von 
        einer Gruppe, die viel, viel kleiner ist als die Vernünftigen 
        in diesem Land", sagte Klingbeil.
        """

        summary = self.summarizer.summarize(text)

        # todo actually useful tests
        self.assertNotEqual(summary, "")
        self.assertIsNotNone(summary)

        text2 = """
        Tausende protestieren in Berlin und Potsdam gegen Rechtsextremismus
        "Demokratie verteidigen" – in Berlin rufen Fridays for Future zu einer Demo am Brandenburger Tor. In Potsdam gehen auch Olaf Scholz und Annalena Baerbock auf die Straße. 
        """
        summary2 = self.summarizer.summarize(text2)
        self.assertNotEqual(summary2, "")
        self.assertIsNotNone(summary2)


if __name__ == '__main__':
    unittest.main()
