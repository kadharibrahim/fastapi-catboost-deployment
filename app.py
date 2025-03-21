from fastapi import FastAPI
import catboost
import numpy as np
import json

app = FastAPI()

# Load trained model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")  # Ensure model file is correct

@app.post("/predict/")
def predict(data: dict):
    try:
        features = np.array(data["features"]).reshape(1, -1)  # Ensure correct shape

        # Debugging: Print received input
        print("Received Features:", features)

        # Validate feature length
        if features.shape[1] != len(model.feature_names_):
            return {"error": f"Expected {len(model.feature_names_)} features, but got {features.shape[1]}"}

        # Make prediction
        prediction = model.predict(features)
        return {"fare_amount": prediction.tolist()}

    except Exception as e:
        return {"error": str(e)}
