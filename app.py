import os
import sys 
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = "mongodb+srv://rohit2005_ds:Rohit2205@cluster0.wnq2ejc.mongodb.net/?appName=Cluster0"
print(mongo_db_url)
import pymongo
from networksecurity.exceptions.exception import NetworkSecurityException
from networksecurity.loggings.loggers import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run 
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./templates")

client = pymongo.MongoClient(mongo_db_url,tlsCAFile = ca)

database = client[DATA_INGESTION_DATABASE_NAME]
collection = client[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training completed succesfully")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request:Request,file:UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        print(df)
        preprocessor = load_object("final_models/preprocessing.pkl")
        final_model = load_object("final_models/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-stripped')
        return templates.TemplateResponse("table.html", {"request":request,"table":table_html})
    except Exception as e:
        raise NetworkSecurityException(sys,e)
    
if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)
    