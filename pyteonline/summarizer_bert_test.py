import unittest
from summarizer_bert import BertSummarizer


class TestBertSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = BertSummarizer()

    def test_summarize_not_empty(self):
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

        print(summary)

        # todo actually useful tests
        self.assertNotEqual(summary, "")
        self.assertIsNotNone(summary)


if __name__ == '__main__':
    unittest.main()
