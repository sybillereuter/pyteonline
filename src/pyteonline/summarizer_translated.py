# Idea:
# Alcantara, T.H.M.; Krütli, D.; Ravada, R.; Hanne, T.
# Multilingual Text Summarization for German Texts Using Transformer Models.
# Information 2023, 14, 303.
# https://doi.org/10.3390/info14060303

from .translator import Translator
from summarizer_bart_large_cnn import BartCNNSummarizer


class TranslationSummarizer:
    def __init__(self):
        self.translator = Translator()
        self.summarizer = BartCNNSummarizer()

    def summarize(self, text):
        translation = self.translator.german_to_english(text)
        english_summary = self.summarizer.summarize(translation)
        return self.translator.english_to_german(english_summary)
