import sys
from pathlib import Path

# Ensure project `src` directory is on sys.path so package imports work
project_root = Path(__file__).resolve().parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from textSummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textSummarizer.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from textSummarizer.logging import logger


STAGE_NAME = "Data Ingestion stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} STARTED <<<<<<")
    data_ingestion =  DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE_NAME} COMPLETED <<<<<<\n\nx=========x")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Data Validation stage"

try:
    logger.info(f">>>>>> stage {STAGE_NAME} STARTED <<<<<<")
    data_validation =  DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>>> stage {STAGE_NAME} COMPLETED <<<<<<\n\nx=========x")
except Exception as e:
    logger.exception(e)
    raise e