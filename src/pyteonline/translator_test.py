import unittest
from .translator import Translator


class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = Translator()

    def test_german_to_english(self):
        article = """
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
        translation = self.translator.german_to_english(article)
        print(translation)
        # todo actually useful tests

        self.assertNotEqual(translation, "")
        self.assertIsNotNone(translation)

    def test_english_to_german(self):
        article = """
        "The right-wing extremists have set out to divide this country,"
        said SPD leader Lars Klingbeil on Sunday in the ARD –
        everyone should bear the responsibility to oppose it.
        "First of all, I want them to rise up, to be loud,"
        said Klingbeil. After the corrective revelations, no one can remain silent.
        On the contrary, "those who are just calm should also raise their voices
        loudly and say: We do not allow this country to be so polarized and
        divided by a group that is much, much smaller than the reasonable ones
        in this country," said Klingbeil.
        """
        translation = self.translator.english_to_german(article)
        print(translation)
        # todo actually useful tests
        self.assertNotEqual(translation, "")
        self.assertIsNotNone(translation)


if __name__ == '__main__':
    unittest.main()
