from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.loggers import logging
from scipy.stats import ks_2samp     #ks_2samp is use to find the drift in the data
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

import pandas as pd
import os,sys

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                     data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            logging.info(f"Required number of columns :{number_of_columns}")
            logging.info(f"Number of Columns Dataframe have :{dataframe.columns}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_datatypes(self,dataframe:pd.DataFrame) -> bool:
        try:
            for col in self._schema_config:
                if col not in dataframe.columns:
                    return False
                if not pd.api.types.is_integer_dtype(dataframe[col]):
                    return False
                
            return True
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def detect_dataset_drift(self,base_df,current_df,threshold = 0.05) -> bool:
        try:
            status = True
            report ={}

            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_distribution = ks_2samp(d1,d2)

                if threshold <= is_same_distribution.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
            report.update({column:{
                        "p_value":float(is_same_distribution.pvalue),
                        "drift_status":is_found
            }})       
                    

        except Exception as e:
            raise NetworkSecurityException(e,sys)  

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## Read data 
            trained_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## validate no of columns

            status = self.validate_number_of_columns(trained_dataframe)
            if not status:
                error_message = f"The training data does not consist of all the columns\n"
            status = self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message = f"The test data does not consist of all the columns\n"

            ## validate datatype 
            
            status = self.validate_datatypes(trained_dataframe)
            if not status:
                error_message = f"All the columns in the train data are not of Integer dataype\n"

            status = self.validate_datatypes(test_dataframe)
            if not status:
                error_message = f"All the columns in the test data are not of Integer dataype\n"

            ## checking the data drift 

            status = self.detect_dataset_drift(base_df=trained_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            trained_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_train_file_path= self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)  

        

    
        




