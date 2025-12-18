from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.loggers import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataTransformationArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataIngestionConfig,DataTransformationConfig,DataValidationConfig,TrainingPipelineConfig

import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("data ingestion completed")
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("Initiate the data validation")
        datavalidationartifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(datavalidationartifact)
        data_transformation_config = DataTransformationConfig(trainingpipelineconfig)
        logging.info("entering data transformation")
        data_transformation = DataTransformation(DataValidationArtifact,DataTransformationConfig)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info("Data Transformation is completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
