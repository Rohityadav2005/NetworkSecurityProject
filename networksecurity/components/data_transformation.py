import sys
import os
import pandas as pd
import numpy as np 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.loggers import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifact,
                data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifacts:DataValidationArtifact = data_validation_artifacts
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod

    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def get_data_transformer_object(cls)-> Pipeline:
        '''
        It initiates the KNNimputer with the parameter in the training_pipeline.py and returns the Pipeline Object as the first step
         Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        '''
        logging.info("entered the get_data_transformation_object in the DataTransformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialize KNNimputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline = Pipeline([("imputer",imputer)])
            return processor

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self) -> DataValidationArtifact:
        logging.info("Entering the initiate_data_transformation method in DataTransformation class")
        try:
            logging.info("starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)

            #training Dataframe
            input_feature_train_df = train_df.drop[TARGET_COLUMN]
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            #test Dataframe 
            input_feature_test_df = test_df.drop[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train = preprocessor.transform(input_feature_train_df)
            transformed_input_feature_test = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_feature_train,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_feature_train,np.array(target_feature_test_df)]

            # save numpy array data 

            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object,)

            # Preparing Artifact

            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            
            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)



    