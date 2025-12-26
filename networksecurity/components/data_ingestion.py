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
from networksecurity.entity.artifact_entity import DataIngestionArtifact

MONGO_DB_URL = "mongodb+srv://rohit2005_ds:Rohit2205@cluster0.wnq2ejc.mongodb.net/?appName=Cluster0"
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            records = list(collection.find())
            print(f"Database: {database_name}, Collection: {collection_name}, Count: {len(records)}")

            df = pd.DataFrame(records)
            print(f"DEBUG: Found {len(df)} records in MongoDB collection '{collection_name}'")

            if df.empty:
               raise Exception("DataFrame is empty! Check your MongoDB data.")
        
            if "_id" in df.columns.to_list():
                df = df.drop(columns="_id",axis=1)
                df.replace({"na":np.nan},inplace=True)

            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            
    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_filepath
            # creating folder
            dir_path = os.path.dirname(feature_store_file_path) 
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe

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
            train_set.to_csv(self.data_ingestion_config.training_file_path,index = False,header = True)
            test_set.to_csv(self.data_ingestion_config.test_file_path,index = False,header = True)
            logging.info("exporting train and test file path")

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.test_file_path)
            return dataingestionartifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)