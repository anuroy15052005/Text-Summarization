from textSummarizer.constants import *
from textSummarizer.utils.common import read_yaml, create_directories
from textSummarizer.entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig)

from pathlib import Path
from types import SimpleNamespace


def _to_namespace(obj):
    """Recursively convert dicts to objects with attribute access."""
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: _to_namespace(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_to_namespace(i) for i in obj]
    return obj


class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH):

        # Resolve relative paths against the project root so the code
        # works regardless of current working directory (e.g., notebooks).
        base_dir = Path(__file__).resolve().parents[3]
        config_path = Path(config_filepath)
        params_path = Path(params_filepath)
        if not config_path.is_absolute():
            config_path = base_dir / config_path
        if not params_path.is_absolute():
            params_path = base_dir / params_path

        self.config = read_yaml(config_path)
        self.params = read_yaml(params_path)

        # if read_yaml returned plain dicts (fallback mode), convert to objects
        if isinstance(self.config, dict):
            self.config = _to_namespace(self.config)
        if isinstance(self.params, dict):
            self.params = _to_namespace(self.params)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir 
        )

        return data_ingestion_config
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            tokenizer_name=config.tokenizer_name,
        )

        return data_transformation_config


    def get_model_trainer_config(self) -> ModelTrainerConfig:
            config = self.config.model_trainer
            params = self.params.TrainingArguments
    
            create_directories([config.root_dir])
    
            model_trainer_config = ModelTrainerConfig(
                root_dir=config.root_dir,
                data_path=config.data_path,
                model_ckpt = config.model_ckpt,
                num_train_epochs = params.num_train_epochs,
                warmup_steps = params.warmup_steps,
                per_device_train_batch_size = params.per_device_train_batch_size,
                weight_decay = params.weight_decay,
                logging_steps = params.logging_steps,
                evaluation_strategy = params. evaluation_strategy,
                eval_steps = params. evaluation_strategy,
                save_steps = params. save_steps,
                gradient_accumulation_steps = params.gradient_accumulation_steps
            )
    
            return model_trainer_config