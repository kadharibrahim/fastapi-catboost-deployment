from fastapi import FastAPI
import catboost
import numpy as np
from pydantic import BaseModel

# Load the trained CatBoost model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")

# ✅ Remove cat_features if they are not needed
model._object._cat_features = None  # <-- Fix the issue

# Initialize FastAPI app
app = FastAPI()

# Define request format
class PredictionRequest(BaseModel):
    features: list  # Input should be a list of numerical features

@app.post("/predict/")
def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)  # Convert input to NumPy array
    prediction = model.predict(features)  # Make prediction
    return {"prediction": float(prediction)}
