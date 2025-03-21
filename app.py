from fastapi import FastAPI
from pydantic import BaseModel
import catboost
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Load the trained CatBoost model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")  # Ensure this file exists

# Categorical feature indices
cat_features_indices = [4, 5]

class InputData(BaseModel):
    features: list

@app.post("/predict/")
def predict(data: InputData):
    try:
        # Convert input to numpy array
        features = np.array([data.features], dtype=object)  # Use dtype=object for mixed types

        # Convert categorical features to string type
        for i in cat_features_indices:
            features[:, i] = features[:, i].astype(str)

        # Create CatBoost Pool object
        test_pool = catboost.Pool(data=features, cat_features=cat_features_indices)

        # Make prediction
        prediction = model.predict(test_pool)

        return {"prediction": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}
