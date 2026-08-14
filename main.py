import sys
import os
from pathlib import Path


project_root = Path(__file__).resolve().parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from textSummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textSummarizer.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from textSummarizer.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from textSummarizer.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline
from textSummarizer.logging import logger


STAGE_NAME = "Data Ingestion stage"
train_data_path = "artifacts/data_ingestion/samsum_dataset/train"
try:
    if os.path.exists(train_data_path):
        logger.info(f">>>>>> stage {STAGE_NAME} SKIPPED (data already exists) <<<<<<")
    else:
        logger.info(f">>>>>> stage {STAGE_NAME} STARTED <<<<<<")
        data_ingestion = DataIngestionTrainingPipeline()
        data_ingestion.main()
        logger.info(f">>>>>> stage {STAGE_NAME} COMPLETED <<<<<<\n\nx=========x")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Data Validation stage"
status_file = Path("artifacts/data_validation/status.txt")
try:
    skip = False
    if status_file.exists():
        with open(status_file, 'r') as f:
            content = f.read()
        if "True" in content:
            skip = True

    if skip:
        logger.info(f">>>>>> stage {STAGE_NAME} SKIPPED (validation already passed) <<<<<<")
    else:
        logger.info(f">>>>>> stage {STAGE_NAME} STARTED <<<<<<")
        data_validation = DataValidationTrainingPipeline()
        data_validation.main()
        logger.info(f">>>>>> stage {STAGE_NAME} COMPLETED <<<<<<\n\nx=========x")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Data Transformation stage"
transformed_data_path = Path("artifacts/data_transformation/samsum_dataset/train")
try:
    if transformed_data_path.exists():
        logger.info(f">>>>>> stage {STAGE_NAME} SKIPPED (transformed data already exists) <<<<<<")
    else:
        logger.info(f">>>>>> stage {STAGE_NAME} STARTED <<<<<<")
        data_transformation = DataTransformationTrainingPipeline()
        data_transformation.main()
        logger.info(f">>>>>> stage {STAGE_NAME} COMPLETED <<<<<<\n\n x=========x")
except Exception as e:
    logger.exception(e)
    raise e



STAGE_NAME = "Model Trainer stage"
model_path = "artifacts/model_trainer/pegasus-samsum-model/model.safetensors"
try:
    if os.path.exists(model_path):
        logger.info(f">>>>>> stage {STAGE_NAME} SKIPPED (model already exists) <<<<<<")
    else:
        logger.info(f"**********************")
        logger.info(f">>>>>> stage {STAGE_NAME} STARTED <<<<<<")
        model_trainer = ModelTrainerTrainingPipeline()
        model_trainer.main()
        logger.info(f">>>>>> stage {STAGE_NAME} COMPLETED <<<<<<\n\n x=========x")
except Exception as e:
    logger.exception(e)
    raise e

