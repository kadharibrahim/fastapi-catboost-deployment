from fastapi import FastAPI
import catboost
import numpy as np
from pydantic import BaseModel

# Load the trained CatBoost model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")
print("✅ Model Loaded Successfully!")  # Add this line

# Initialize FastAPI app
app = FastAPI()

# Define request format
class PredictionRequest(BaseModel):
    features: list  # Ensure input is a list of numerical values

@app.post("/predict/")
def predict(request: PredictionRequest):
    try:
        features = np.array(request.features).reshape(1, -1)  # Convert to NumPy array
        print("🔹 Received Features:", features)  # Debugging print
        prediction = model.predict(features)  # Make prediction
        print("🔹 Prediction:", prediction)  # Debugging print
        return {"prediction": float(prediction)}
    except Exception as e:
        print("❌ Error:", str(e))  # Debugging print
        return {"error": str(e)}
