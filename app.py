from fastapi import FastAPI
import catboost
import numpy as np

app = FastAPI()

# Load CatBoost model
model = catboost.CatBoostRegressor()
model.load_model("deployed_catboost_model.cbm")  # Ensure correct model path

# Define categorical feature indices (update based on your data)
CATEGORICAL_FEATURES = [4, 5]  # Update this based on your model training

@app.post("/predict/")
def predict(features: dict):
    try:
        # Convert input features to numpy array
        feature_values = np.array(features["features"]).reshape(1, -1)

        # Create CatBoost Pool object with categorical features
        test_pool = catboost.Pool(feature_values, cat_features=CATEGORICAL_FEATURES)

        # Make prediction
        prediction = model.predict(test_pool)

        return {"prediction": prediction.tolist()}
    except Exception as e:
        return {"error": str(e)}
