🚀 FastAPI CatBoost Deployment
📌 Overview
This repository contains a FastAPI application that serves a CatBoost machine learning model for predicting Uber ride fares. The model expects 35 input features and returns a fare prediction.

✅ Built with: FastAPI, CatBoost, Uvicorn
✅ Deployed on: Render

🌍 Live API URL
🔗 Base URL: https://fastapi-catboost-deployment.onrender.com

📌 Interactive Docs (Swagger UI):
🔗 https://fastapi-catboost-deployment.onrender.com/docs

📌 OpenAPI JSON Schema:
🔗 https://fastapi-catboost-deployment.onrender.com/openapi.json

🛠️ How to Use the API
🔹 1. Make a Prediction
📌 Method: POST
📌 Endpoint: /predict/
📌 Content-Type: application/json

🔹 Request Format
Send a JSON payload with exactly 35 features inside the "features" array.

json
Copy
Edit
{
  "features": [
    3.2, 0, 1, 9.6, 12, 45, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  ]
}
🔹 Response Format
📌 Success Response (200 OK)

json
Copy
Edit
{
  "prediction": [275.87]
}
📌 Error Response (400 Bad Request)

json
Copy
Edit
{
  "error": "Expected 35 features, but got 34"
}
📌 Error Response (422 Unprocessable Entity)

json
Copy
Edit
{
  "error": "'data' is numpy array of floating point numerical type, it means no categorical features, but 'cat_features' parameter specifies nonzero number of categorical features"
}
📌 Testing the API
🔹 Option 1: Swagger UI
Visit https://fastapi-catboost-deployment.onrender.com/docs and test the /predict/ endpoint interactively.

🔹 Option 2: Python Script
Run this script to test the API:

python
Copy
Edit
import requests

url = "https://fastapi-catboost-deployment.onrender.com/predict/"
data = {
    "features": [3.2, 0, 1, 9.6, 12, 45, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())
🔹 Option 3: cURL Command
Run this in a terminal:

sh
Copy
Edit
curl -X 'POST' \
  'https://fastapi-catboost-deployment.onrender.com/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "features": [3.2, 0, 1, 9.6, 12, 45, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}'
📂 Project Structure
bash
Copy
Edit
📦 fastapi-catboost-deployment
 ┣ 📜 app.py               # FastAPI application
 ┣ 📜 deployed_catboost_model.cbm  # Trained CatBoost model
 ┣ 📜 requirements.txt      # Dependencies
 ┣ 📜 Procfile             # Deployment script (for Render)
 ┣ 📜 README.md            # API documentation (this file)
 ┗ 📜 .gitignore           # Ignore unnecessary files
🚀 Deployment & Hosting
✅ Deployed on: Render
✅ Model: CatBoost Regressor
✅ Auto-deploy enabled: Updates pushed to GitHub redeploy automatically.

💡 Future Improvements
🔹 Improve model performance.
🔹 Add authentication for secured API access.
🔹 Build a front-end UI to interact with the API.

📬 Contact & Support
👤 Developer: Kadhar Ibrahim
📧 Email: kadharibrahim0@gmail.com
🔗 GitHub Repo: fastapi-catboost-deployment

⭐ If you find this project useful, don't forget to give it a star! ⭐
Happy coding! 🚀🎯
