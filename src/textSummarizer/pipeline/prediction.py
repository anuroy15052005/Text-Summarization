from textSummarizer.config.configuration import ConfigurationManager
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()

    def predict(self, text):
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path)

        inputs = tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")

        summary_ids = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            length_penalty=0.8,
            num_beams=8,
            max_length=60,
            min_length=10,
            no_repeat_ngram_size=3,
            repetition_penalty=2.5,
            early_stopping=True
        )

        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return output