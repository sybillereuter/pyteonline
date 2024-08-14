import re
import warnings
from transformers import pipeline
from transformers.utils import logging

logging.set_verbosity_error()
warnings.filterwarnings("ignore",
                        message="Using the model-agnostic default `max_length`"
                        )


class T5Summarizer:
    def __init__(self):
        self.summarization_pipeline = pipeline("summarization", model="T-Systems-onsite/mt5-small-sum-de-en-v2")

    def summarize(self, text):
        if len(text) < 50:
            return text
        summary = self.summarization_pipeline(text, min_length=50, max_length=200, num_beams=4)[0]['summary_text']
        summary = self.remove_duplicate_sentences(summary)
        return summary

    @staticmethod
    def remove_duplicate_sentences(text: str) -> str:
        sentences = re.split(r'(?<!\d)\.(?!\d)', text)
        seen = set()
        unique_sentences = [
            sentence.strip() for sentence in sentences
            if sentence.strip() and sentence not in seen and not seen.add(sentence)
        ]
        return '. '.join(unique_sentences).strip() + '.'
