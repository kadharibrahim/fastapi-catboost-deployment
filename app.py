from fastapi import FastAPI
import catboost
import numpy as np
from pydantic import BaseModel

# Load the trained CatBoost model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")
print("✅ Model Loaded Successfully!")

# 🚀 Fix: Ensure no categorical features
model._init_params["cat_features"] = None  

# Initialize FastAPI app
app = FastAPI()

# Define request format
class PredictionRequest(BaseModel):
    features: list  # Ensure input is a list of numerical values

@app.post("/predict/")
def predict(request: PredictionRequest):
    try:
        features = np.array(request.features).reshape(1, -1)  # Convert to NumPy array
        print("🔹 Received Features:", features)  
        
        # 🔥 Fix: Predict with numerical-only input
        prediction = model.predict(features)  
        
        print("🔹 Prediction:", prediction)  
        return {"prediction": float(prediction)}
    except Exception as e:
        print("❌ Error:", str(e))  
        return {"error": str(e)}