import os
from textSummarizer.logging import logger
from textSummarizer.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        try:
            from transformers import AutoTokenizer
        except ImportError as exc:
            raise ImportError(
                "Missing dependency 'transformers'. Install it with `pip install transformers[sentencepiece]` "
                "or `pip install -r requirements.txt`."
            ) from exc

        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(
            example_batch['dialogue'], max_length=1024, truncation=True
        )

        target_encodings = self.tokenizer(
            text_target=example_batch['summary'], max_length=128, truncation=True
        )

        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids'],
        }

    def convert(self):
        try:
            from datasets import load_from_disk
        except ImportError as exc:
            raise ImportError(
                "Missing dependency 'datasets'. Install it with `pip install datasets` "
                "or `pip install -r requirements.txt`."
            ) from exc

        dataset_samsum = load_from_disk(self.config.data_path)
        dataset_samsum_pt = dataset_samsum.map(
            self.convert_examples_to_features,
            batched=True,
            remove_columns=dataset_samsum['train'].column_names,
        )
        dataset_samsum_pt.save_to_disk(os.path.join(self.config.root_dir, "samsum_dataset"))

