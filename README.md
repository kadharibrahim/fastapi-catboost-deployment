# 🚀 Real-time-fare-prediction: Uber Fare Prediction API

This project demonstrates a full ML workflow—from data analysis to deploying a CatBoost regression model using FastAPI. It predicts Uber ride fares based on trip features like time, location, and more. Ideal for learning and showcasing real-world machine learning deployment.

---

## 🌟 Live Demo

Experience the real-time Uber fare prediction app here:  
👉 [https://fastapi-catboost-deployment-ibiuv.streamlit.app/](https://fastapi-catboost-deployment-ibiuv.streamlit.app/)

---

## 📘 Table of Contents

- 📌 Overview  
- 🧠 Project Highlights  
- 🌟 Features Involved  
- 🗂️ Directory Structure  
- 🔍 Exploratory Data Analysis  
- 📦 Model Deployment with FastAPI  
- 🚀 Getting Started  
- 🌐 API Documentation  
- ☁️ Deployment on Render  
- 📊 Example Predictions  
- 🎯 Use Cases  
- 🛠️ Tech Stack  
- 🙌 Acknowledgements  
- 📜 License  

---

## 📌 Overview

This project demonstrates:
- Real-time fare prediction using FastAPI
- A trained and deployed CatBoost regression model
- Cleaned and feature-engineered Uber ride data
- Exploratory data analysis and model training in Jupyter
- REST API endpoint for prediction
- Production-ready structure with `Procfile` and `requirements.txt`

---

## 🧠 Project Highlights

| Feature               | Description                                             |
|-----------------------|---------------------------------------------------------|
| 🧠 ML Model           | CatBoost Regressor trained on curated Uber ride data    |
| 📊 EDA & Preprocessing| In-depth analysis in `uber_analysis.ipynb`              |
| ⚡ Realtime Prediction | REST API using FastAPI                                  |
| 🌍 Deployment         | Render-ready via `Procfile`                              |
| 🛡️ Robustness         | Error handling, validation, clean architecture           |
| 🧪 Testing            | Swagger UI for API testing and interaction              |

---

## 🌟 Features Involved

- **Interactive User Interface with Streamlit**  
  A user-friendly web interface built using Streamlit, allowing users to input trip details and receive fare predictions instantly.

- **FastAPI Backend Integration**  
  The Streamlit frontend communicates with a FastAPI backend, which handles the prediction logic and serves the CatBoost model.

- **CatBoost Regression Model**  
  Utilizes a trained CatBoost regressor to predict Uber ride fares based on input features such as pickup/dropoff locations, time, and distance.

- **Real-Time Predictions**  
  Provides immediate fare predictions upon user input, demonstrating real-time machine learning inference.

- **Deployment on Streamlit Cloud**  
  The entire application is deployed on Streamlit Cloud, ensuring accessibility and scalability without the need for complex infrastructure.

---

## 📁 Directory Structure

uber-fare-prediction-fastapi/ ├── app.py # FastAPI app for model inference ├── deployed_catboost_model.cbm # Trained CatBoost model ├── uber_analysis.ipynb # Jupyter Notebook for EDA & training ├── requirements.txt # Project dependencies ├── Procfile # Deployment config for Render └── README.md # Project documentation (this file)

yaml
Copy
Edit

---

## 🔍 Exploratory Data Analysis (EDA)

Contained in [`uber_analysis.ipynb`](./uber_analysis.ipynb):
- **Data Cleaning:** Handling missing values, outlier detection
- **Feature Engineering:** Time-of-day extraction, location categorization
- **Visualization:** Fare vs. distance, pickup time heatmaps
- **Model Evaluation:** RMSE, MAE, R² metrics on test data
- **Model Export:** Saved using `.save_model()` in CatBoost

---

## 📦 Model Deployment with FastAPI

`app.py` contains the FastAPI app that:
- Loads the trained `.cbm` model at startup
- Accepts POST requests with JSON-formatted input features
- Uses CatBoost's `Pool()` with specified categorical indices
- Returns a prediction with structured JSON output

```python
@app.post("/predict/")
def predict(features: dict):
    ...
Example input:
json
Copy
Edit
{
  "features": [2.0, 5.0, 0.5, 1.2, "Manhattan", "JFK"]
}
🚀 Getting Started
🔧 Prerequisites:
Python 3.8+

Git

1. Clone the repository
bash
Copy
Edit
git clone https://github.com/your-username/uber-fare-prediction-fastapi.git
cd uber-fare-prediction-fastapi
2. Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run the FastAPI app
bash
Copy
Edit
uvicorn app:app --reload
Access it at: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs

🌐 API Documentation
Endpoint: /predict/

Method: POST

Request Body: JSON

Response: JSON with fare prediction

✅ Request Format:

json
Copy
Edit
{
  "features": [pickup_hour, day_of_week, distance_km, duration_min, pickup_area, dropoff_area]
}
🔁 Sample Response:

json
Copy
Edit
{
  "prediction": [18.45]
}
☁️ Deployment on Render
Push your code to GitHub

Go to https://render.com

Create a New Web Service

Build Command: pip install -r requirements.txt

Start Command: uvicorn app:app --host 0.0.0.0 --port $PORT

Add Procfile with content:

less
Copy
Edit
web: uvicorn app:app --host 0.0.0.0 --port $PORT
📊 Example Predictions
Try in Swagger UI /docs or using curl:

bash
Copy
Edit
curl -X POST http://localhost:8000/predict/ -H "Content-Type: application/json" -d '{"features": [15, 2, 8.3, 24, "Manhattan", "JFK"]}'
Response:

json
Copy
Edit
{"prediction": [32.75]}
🎯 Use Cases
📱 Uber fare estimation app backend

🧠 Real-time regression API showcase

📊 Model deployment tutorial for ML learners

🧪 Experimentation platform for feature engineering

💼 Resume project for machine learning engineers

🛠️ Tech Stack
Language: Python 3.8+

Framework: FastAPI

Frontend: Streamlit

ML Model: CatBoost Regressor

Visualization: Matplotlib, Pandas

Deployment: Render + Streamlit Cloud

Testing: Swagger / Curl / Postman

🙌 Acknowledgements
CatBoost by Yandex

FastAPI by Sebastián Ramírez

Dataset inspired by Uber open trip data

📜 License
This project is licensed under the MIT License.

⭐️ Show Your Support
If you found this project helpful:

🌟 Star this repository

🍴 Fork it for your own use

🧑‍💻 Connect with me on linkedin.com/in/kadharibrahim

📬 Raise issues or ideas for improvements

“Building real-time, intelligent systems is no longer optional—it's the future.”
— Kadhar Ibrahim 🚀 | 💡 Data Enthusiast | 🧠 ML Explorer | 🔧 Problem Solver

yaml
Copy
Edit

---

Let me know if you want this split into separate sections, or turned into an actual `.md` file for download!
