import unittest
from .summarizer_t5 import T5Summarizer


class TestT5Summarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = T5Summarizer()

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
        # print(summary)
        # todo actually useful tests
        self.assertNotEqual(summary, "")
        self.assertIsNotNone(summary)

        text2 = """
                Tausende protestieren in Berlin und Potsdam gegen Rechtsextremismus
                "Demokratie verteidigen" – in Berlin rufen Fridays for Future zu einer Demo am Brandenburger Tor. In Potsdam gehen auch Olaf Scholz und Annalena Baerbock auf die Straße. 
                """
        summary2 = self.summarizer.summarize(text2)
        print(summary2)

        print(self.summarizer.remove_duplicate_sentences("""Die Europäische Zentralbank hat 
        in ihrer ersten Geldpolitischen Entscheidung 
        im neuen Jahr den Leitzins unverändert gelassen. 
        Damit bleibt der Zins auf dem Stand von 4,5 Prozent. Damit bleibt der Zins auf dem Stand von 4,5 Prozent."""))

    def test_remove_dupes(self):
        print(self.summarizer.remove_duplicate_sentences("""Die Europäische Zentralbank hat 
               in ihrer ersten Geldpolitischen Entscheidung 
               im neuen Jahr den Leitzins unverändert gelassen. 
               Damit bleibt der Zins auf dem Stand von 4,5 Prozent. Damit bleibt der Zins auf dem Stand von 4,5 Prozent."""))



if __name__ == '__main__':
    unittest.main()
