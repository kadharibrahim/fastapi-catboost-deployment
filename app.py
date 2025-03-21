from fastapi import FastAPI
import catboost
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the trained CatBoost model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")  # Ensure the correct model file is loaded

# Specify categorical feature indices (example: columns 4 and 5)
cat_features_indices = [4, 5]  

@app.post("/predict/")
def predict(features: dict):
    try:
        feature_values = np.array(features["features"]).reshape(1, -1)  # Ensure 2D input
        test_pool = catboost.Pool(data=feature_values, cat_features=cat_features_indices)
        prediction = model.predict(test_pool)  # Make prediction
        return {"prediction": prediction.tolist()}  
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def home():
    return {"message": "FastAPI is running and the CatBoost model is loaded!"}
