import os
import sys
import pandas as pd
import numpy as np 

TARGET_COLUMN = 'Result'
PIPELINE_NAME : str = 'NetworkSecurity'
ARTIFACTS_DIR : str = 'Artifacts'
FILE_NAME : str = 'phisingData.csv'

TRAIN_DATA_NAME : str = 'train.csv'
TEST_DATA_NAME : str = 'test.csv'

SCHEMA_FILE_PATH: os.path.join("data_schema","schema.yaml")
 ## data ingestion variables
DATA_INGESTION_COLLECTION_NAME : str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME : str = 'DS_Rohit'
DATA_INGESTION_DIR_NAME : str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR : str = 'feature_store'
DATA_INGESTION_INGESTED_DIR : str = 'Ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION : float = 0.2

## data validation variables

DATA_VALIDATION_DIR_NAME: str = "data_validation" 
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

## data transformation variables

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_obj"

## imputer class
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values" : np.nan,
    "n_neighbors" : 3,
    "weights" : "uniform",
}



