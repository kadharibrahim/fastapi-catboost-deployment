from fastapi import FastAPI
import catboost
import numpy as np
from pydantic import BaseModel

# Load the model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")

print("✅ Model Loaded Successfully!")

# Initialize FastAPI app
app = FastAPI()

# Define request format
class PredictionRequest(BaseModel):
    features: list  # Ensure input is a list of numerical features

@app.post("/predict/")
def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)  # Convert input to NumPy array
    prediction = model.predict(features)  # Make prediction
    return {"prediction": float(prediction)}

# Run API using:
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload
    