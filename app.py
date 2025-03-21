from fastapi import FastAPI
import catboost
import numpy as np
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Load the trained model
model = catboost.CatBoostRegressor()

try:
    model.load_model("deployed_catboost_model.cbm")
    print("✅ Model Loaded Successfully!")
except Exception as e:
    print("❌ Model Loading Failed:", str(e))

# Ensure model does not expect categorical features
model._object._cat_features = []

# Define request format
class PredictionRequest(BaseModel):
    features: list  # Input should be a list of numerical features

@app.post("/predict/")
def predict(request: PredictionRequest):
    print("📥 Received Features:", request.features)  # Debugging input
    
    try:
        features = np.array(request.features).reshape(1, -1)  # Convert to NumPy array
        prediction = model.predict(features)  # Make prediction
        print("📤 Prediction:", prediction)  # Debugging output
        
        return {"prediction": float(prediction)}
    
    except Exception as e:
        print("❌ Prediction Error:", str(e))
        return {"error": str(e)}

# Run API using: uvicorn app:app --host 0.0.0.0 --port 8000 --reload