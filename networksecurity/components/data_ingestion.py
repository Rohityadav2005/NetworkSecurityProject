from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.loggers import logging

from sklearn.model_selection import train_test_split
import os
import numpy as np 
import pandas as pd
import sys
import pymongo
from typing import List
from networksecurity.entity.config_entity import DataIngestionConfig

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection= self.mongo_client[database_name],[collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns="_id",axis=1)
                df.replace({"na":np.nan},inplace=True)

                return df
        except Exception as e:
            NetworkSecurityException(e,sys)

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_filepath
            # creating folder
            dir_path = os.path.dirname(feature_store_file_path) 
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("performed train test split")
            logging.info("Exited split_data_as_train_test method in the DataIngestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index = False,heading = True)
            test_set.to_csv(self.data_ingestion_config.training_file_path,index = False,heading = True)
            logging.info("exporting train and test file path")

        except Exception as e:
            raise NetworkSecurityException

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)

        except Exception as e:
            raise NetworkSecurityException


        
     

