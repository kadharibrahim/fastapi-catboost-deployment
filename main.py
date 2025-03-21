from fastapi import FastAPI
import catboost
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the trained CatBoost model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")  # Make sure this file is in the same directory

@app.get("/")
def home():
    return {"message": "FastAPI is running and the CatBoost model is loaded!"}

# Run the API using: uvicorn main:app --reload
