import os
import sys
from pathlib import Path

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response, JSONResponse, HTMLResponse
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "final_models"

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        if 'Result' in df.columns:
            df = df.drop(columns=['Result'])

        preprocessor = load_object(str(MODEL_DIR / "preprocessor.pkl"))
        required_columns = list(preprocessor.feature_names_in_)
        missing = [col for col in required_columns if col not in df.columns]
        extra = [col for col in df.columns if col not in required_columns]

        if missing:
            return JSONResponse(status_code=400, content={
                "error": "Missing required columns",
                "missing_columns": missing,
                "required_columns": required_columns
            })

        df = df[required_columns]
        final_model = load_object(str(MODEL_DIR / "model.pkl"))
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return HTMLResponse(content=f"<html><body>{table_html}</body></html>")
    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "traceback": traceback.format_exc().splitlines()
        })

if __name__  == "__main__":
    app_run(app,host="localhost",port=8000)