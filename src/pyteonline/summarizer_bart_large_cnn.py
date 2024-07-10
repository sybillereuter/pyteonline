from transformers import pipeline


class BartCNNSummarizer:
    def __init__(self):
        self.summarization_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text):
        if len(text < 50):
            return text
        summary = self.summarization_pipeline(text, max_length=200, min_length=50, do_sample=False)[0]['summary_text']
        return summary
