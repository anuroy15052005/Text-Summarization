import os
from pathlib import Path
from textSummarizer.logging import logger
from textSummarizer.entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = None

            # Expecting dataset to be under artifacts/data_ingestion/samsum_dataset
            data_dir = Path("artifacts") / "data_ingestion" / "samsum_dataset"
            if not data_dir.exists():
                logger.error(f"Expected data directory not found: {data_dir}")
                validation_status = False
                with open(self.config.STATUS_FILE, 'w') as f:
                    f.write(f"Validation status: {validation_status}")
                return validation_status

            all_files = [p.name for p in data_dir.iterdir() if p.is_dir() or p.is_file()]

            for required in self.config.ALL_REQUIRED_FILES:
                if required not in all_files:
                    validation_status = False
                    break
            else:
                validation_status = True

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            logger.info(f"Validation status: {validation_status}")
            return validation_status

        except Exception as e:
            logger.exception(e)
            raise e
