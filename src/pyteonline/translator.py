from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


class Translator:
    def __init__(self, model_name="facebook/mbart-large-50-many-to-many-mmt"):
        self.model = MBartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

    def german_to_english(self, article):
        return self.translate(article, "de_DE", "en_XX")

    def english_to_german(self, article):
        return self.translate(article, "en_XX", "de_DE")

    def translate(self, article, src_lang, target_lang):
        self.tokenizer.src_lang = src_lang
        encoded_article = self.tokenizer(article, return_tensors="pt")
        forced_bos_token_id = self.tokenizer.lang_code_to_id[target_lang]

        generated_tokens = self.model.generate(
            **encoded_article,
            forced_bos_token_id=forced_bos_token_id
        )

        translation = self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        return translation
