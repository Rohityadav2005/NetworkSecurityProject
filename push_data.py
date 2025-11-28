import os
import sys
from dotenv import load_dotenv
import json
import pymongo
load_dotenv()

import certifi 
co = certifi.where()

import pandas as pd 
import numpy as np 
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings import loggers

class NetworkSecurityExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_converter(self):
        try:
            data = pd.read_csv("C:\Users\rohit\OneDrive\Desktop\RHT-MLProject-2\Network_data\phisingData.csv")
            data.reset_index(drop=True,inplace=True)

            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database,collection):
        self.database = database
        self.records = records
        self.collection = collection

        self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)

        


    
    




