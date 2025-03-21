from fastapi import FastAPI
import catboost
import numpy as np
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Load the trained model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")  # Ensure this file is uploaded in GitHub

# Define request format
class PredictionRequest(BaseModel):
    features: list  # Expecting a list of numerical and categorical values

@app.post("/predict/")
def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)  # Convert to NumPy array
    prediction = model.predict(features)  # Make prediction
    return {"prediction": float(prediction)}

# To run locally: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
