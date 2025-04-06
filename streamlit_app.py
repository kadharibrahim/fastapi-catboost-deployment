import streamlit as st
import requests
import datetime
import random
import pyperclip
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import plotly.express as px

# ✅ Set Page Configuration
st.set_page_config(page_title="Uber Fare Prediction", layout="wide")

# ✅ Set Background Image
page_bg_img = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: url("https://images.unsplash.com/photo-1532375810709-75c1f1e7ad84") no-repeat center center fixed;
    background-size: cover;
}
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.6);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

GOOGLE_MAPS_API_KEY = "AIzaSyAbgA9gFMQo2ccFDTLS0L1oD3o48DQqZoo"
FASTAPI_URL = "https://fastapi-catboost-deployment.onrender.com/predict/"
share_url = "https://your-streamlit-app-url.com"

location_mapping = {
    "Anna Nagar (VR Mall) 🏦": (13.0827, 80.2170, 1),
    "Chennai Central Railway Station (Chennai Central) 🚉": (13.0839, 80.2707, 2),
    "Guindy (Race Course) 🏇": (13.0072, 80.2209, 3),
    "Marina Beach (Marina Beach) 🌊": (13.0495, 80.2820, 4),
    "Perambur (Sri Brindavan Theatre) 🎭": (13.1173, 80.2503, 5),
    "Pallavaram (Pallavaram Market) 🛍️": (12.9687, 80.1481, 6),
    "Vadapalani (Vadapalani Murugan Temple) 🦚": (13.0503, 80.2127, 7),
    "Koyambedu (Koyambedu Market) 🍎": (13.0668, 80.1989, 8),
    "OMR (IT Corridor) 🏢": (12.9279, 80.1362, 9),
    "Ambattur (Industrial Estate) 🏭": (13.1146, 80.1580, 10),
    "Velachery (Phoenix Marketcity) 🛒": (12.9791, 80.2209, 11),
    "Porur (MIOT Hospital) 🏥": (13.0388, 80.1561, 12),
    "Sholinganallur (ECR Beach) 🏖️": (12.8996, 80.2273, 13),
    "Adyar (Adyar Bridge) 🌉": (13.0067, 80.2551, 14),
    "Chennai Airport (International Airport) ✈️": (12.9816, 80.1636, 15),
    "T Nagar (Pondy Bazaar) 🛒": (13.0400, 80.2330, 16),
    "Tambaram (Railway Station) 🚂": (12.9250, 80.1273, 17),
    "Mylapore (Kapaleeshwarar Temple) 🌙": (13.0315, 80.2684, 18),
    "ECR (Long Drive) 🏎️": (12.9719, 80.1393, 19),
    "Medavakkam (Residential Area) 🏠": (12.9165, 80.1852, 20)
}

# Define your columns first
col_title, col_status, col_share = st.columns([0.7, 0.15, 0.15])

# Then use col_title for the animation
with col_title:
    st.markdown("""
    <div style="position: relative; text-align: center;">
        <h1 style="color: black; font-weight: 800; margin-bottom: 10px;">
            AI Ride Estimator – Predict Before You Trip! 💸
        </h1>
        <div class="race-track">
            <div class="race-car">🏎️💨</div>
        </div>
        <audio autoplay loop>
            <source src="https://www.soundjay.com/transportation/car-race-1.mp3" type="audio/mpeg">
        </audio>
    </div>

    <style>
    .race-track {
        position: relative;
        height: 40px;
        overflow: hidden;
    }

    .race-car {
        position: absolute;
        top: 0px;
        right: -70px;
        font-size: 30px;
        animation: zoomcar 4s linear infinite;
    }

    @keyframes zoomcar {
        0% { right: -90px; opacity: 1; }
        90% { opacity: 1; }
        100% { right: 100%; opacity: 0; }
    }
    </style>
    """, unsafe_allow_html=True)

current_datetime = datetime.datetime.now()
pickup_date = current_datetime.date()
pickup_time_obj = current_datetime.time()
hour_of_day = pickup_time_obj.hour
day_of_week = pickup_date.weekday()
is_weekend = day_of_week in [5, 6]  # Saturday or Sunday
is_peak_hour = 7 <= hour_of_day <= 9 or 17 <= hour_of_day <= 20
is_night = hour_of_day >= 20 or hour_of_day < 6

# Choose surge icon
if is_night:
    surge_icon = "🌙 Night Vibes - Calm and Cool"
elif is_peak_hour and is_weekend:
    surge_icon = "🚗 Weekend Rush - Expect High Demand"
elif is_peak_hour:
    surge_icon = "🚦 Peak Hours - Surge Pricing Active"
elif is_weekend:
    surge_icon = "🍿 Weekend Chill -Few Rides"
else:
    surge_icon = "✅ Smooth Ride - Regular Pricing"


# Show surge + share button (fixed with real app URL)
components.html(
    f"""
    <div style="position: fixed; top: 20px; right: 20px; display: flex; align-items: center; z-index: 999;">
        <span style="font-size: 28px; margin-right: 10px;">{surge_icon}</span>
        <button onclick="navigator.clipboard.writeText('{share_url}'); 
                         let tooltip = document.getElementById('tooltip'); 
                         tooltip.innerHTML='Copied!'; 
                         setTimeout(() => tooltip.innerHTML='Copy Link', 2000);"
                style="background-color: #355C7D; border: none; color: white; padding: 8px 12px;
                       text-align: center; font-size: 14px; border-radius: 6px; cursor: pointer;">
            🔗 <span id="tooltip">Copy Link</span>
        </button>
    </div>
    """,
    height=80,
) 
st.write("🎯 **Hit the target, not your wallet – plan with the price estimator.**")

# ✅ Layout
col1, col2, col3 = st.columns([2, 2, 2])

if "show_ride_options" not in st.session_state:
    st.session_state.show_ride_options = False
if "show_best_times" not in st.session_state:
    st.session_state.show_best_times = False

with col1:
    pickup_location = st.selectbox("📍 Pickup Location", list(location_mapping.keys()), index=0)
    dropoff_location = st.selectbox("📍 Drop-off Location", list(location_mapping.keys()), index=1)
    pickup_date = st.date_input("🗓️ Choose Your Day", datetime.date.today())

    now = datetime.datetime.now()
    time_options = [now + datetime.timedelta(minutes=5 * i) for i in range(288)]
    time_labels = [t.strftime("%I:%M %p") for t in time_options]

    pickup_time = st.selectbox("⏰ Select Pickup Time", time_labels, index=0)
    time_obj = datetime.datetime.strptime(pickup_time, "%I:%M %p").time()
    hour_of_day = time_obj.hour
    day_of_week = pickup_date.weekday()

    pickup_lat, pickup_lon, pickup_encoded = location_mapping[pickup_location]
    dropoff_lat, dropoff_lon, dropoff_encoded = location_mapping[dropoff_location]

    distance_km = 10
    is_weekend = 1 if day_of_week in [5, 6] else 0
    is_peak_hour = 1 if (7 <= hour_of_day <= 9 or 17 <= hour_of_day <= 20) else 0
    distance_time_interaction = distance_km * hour_of_day

    day_of_week_features = [1 if i == day_of_week else 0 for i in range(6)]
    hour_of_day_features = [1 if i == hour_of_day else 0 for i in range(23)]

    features = [
        distance_km, is_weekend, is_peak_hour, distance_time_interaction,
        pickup_encoded, dropoff_encoded
    ] + day_of_week_features + hour_of_day_features

    if len(features) != 35:
        st.error(f"❌ Feature count mismatch! Expected 35, got {len(features)}.")

    if pickup_location == dropoff_location:
        st.warning("Unless you're just testing the app (nice move!), pick a new destination. 🎯👍")

    col_estimate, col_best_time = st.columns(2)

    with col_estimate:
        if st.button("🚕 Get Fare Estimate"):
            st.session_state.show_ride_options = True
            st.session_state.show_best_times = False
            data = {"features": features}
            response = requests.post(FASTAPI_URL, json=data)

            if response.status_code == 200:
                result = response.json()
                if "prediction" in result:
                    base_fare = round(result["prediction"][0], 2)
                    st.session_state.auto_fare = base_fare
                    st.session_state.moto_fare = round(base_fare * (0.45 + (random.uniform(0, 0.1))), 2)
                    st.session_state.uber_fare = round(base_fare * (1.14 + (random.uniform(0, 0.1))), 2)

    with col_best_time:
        if st.button("⏳ Best Fare Time"):
            st.session_state.show_ride_options = False
            st.session_state.show_best_times = True
            st.session_state.cheapest_fares = {
                "Moto": {"fare": float("inf"), "time": ""},
                "Auto": {"fare": float("inf"), "time": ""},
                "SUV": {"fare": float("inf"), "time": ""}
            }

            for i, label in enumerate(time_labels[:24]):
                test_time = datetime.datetime.strptime(label, "%I:%M %p").time()
                test_hour = test_time.hour
                test_inter = distance_km * test_hour
                test_peak = 1 if (7 <= test_hour <= 9 or 17 <= test_hour <= 20) else 0

                test_hour_features = [1 if j == test_hour else 0 for j in range(23)]
                test_features = [
                    distance_km, is_weekend, test_peak, test_inter,
                    pickup_encoded, dropoff_encoded
                ] + day_of_week_features + test_hour_features

                if len(test_features) == 35:
                    try:
                        resp = requests.post(FASTAPI_URL, json={"features": test_features})
                        if resp.status_code == 200 and "prediction" in resp.json():
                            base = resp.json()["prediction"][0]
                            moto = round(base * (0.45 + random.uniform(0, 0.1)), 2)
                            auto = round(base, 2)
                            car = round(base * (1.14 + random.uniform(0, 0.1)), 2)

                            if moto < st.session_state.cheapest_fares["Moto"]["fare"]:
                                st.session_state.cheapest_fares["Moto"] = {"fare": moto, "time": label}
                            if auto < st.session_state.cheapest_fares["Auto"]["fare"]:
                                st.session_state.cheapest_fares["Auto"] = {"fare": auto, "time": label}
                            if car < st.session_state.cheapest_fares["SUV"]["fare"]:
                                st.session_state.cheapest_fares["SUV"] = {"fare": car, "time": label}
                    except Exception as e:
                        st.warning(f"Error: {e}")

# ✅ Ride Options OR Best Times Column
with col2:
    if st.session_state.get("show_ride_options", False):
        st.markdown("### 🚘 Choose a ride")
        st.markdown(f"""<div style="border:2px solid black;padding:10px;border-radius:10px;">
            <h3>🏍️ Moto (1-seater)</h3><p>Fast & affordable bike ride</p><h2>₹{st.session_state.moto_fare}</h2>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="border:2px solid black;padding:10px;border-radius:10px;">
            <h3>🛺 Budget Auto</h3><p>Affordable 3-seater ride</p><h2>₹{st.session_state.auto_fare}</h2>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="border:2px solid black;padding:10px;border-radius:10px;">
            <h3>🚗 Uber SUV</h3><p>Spacious 7-seater car ride</p><h2>₹{st.session_state.uber_fare}</h2>
        </div>""", unsafe_allow_html=True)

    elif st.session_state.get("show_best_times", False):
        st.markdown("### 🕒 Best Times to Ride Smart!")
        
        for ride_type, emoji in zip(["Moto", "Auto", "SUV"], ["🏍️", "🛺", "🚗"]):
            fare = st.session_state.cheapest_fares[ride_type]["fare"]
            time = st.session_state.cheapest_fares[ride_type]["time"]

            st.markdown(f"""
            <div style="border: 2px solid #d9d9d9; border-radius: 15px; padding: 15px; margin-bottom: 15px;
                        background-color: #f9f9f9; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
                <h3 style="margin-bottom: 5px;">{emoji} {ride_type}</h3>
                <p style="font-size: 16px; margin: 5px 0;">
                    <strong>🕓 Best Time:</strong> {time}<br>
                    <strong>💸 Fare:</strong> ₹{fare}
                </p>
            </div>
            """, unsafe_allow_html=True)

# 🎯 Let user guess the fare (just for fun!)
guess = st.slider("🎯 Guess the fare (just for fun!)", min_value=50, max_value=1000, step=10)

# ✨ Button to reveal predicted fare
if st.button("🎲 Reveal Actual Auto Fare"):
    st.write(f"👉 Your guess: ₹{guess}")

    if "auto_fare" in st.session_state:
        predicted_fare = st.session_state.auto_fare
        low = round(predicted_fare * 0.95, 2)
        high = round(predicted_fare * 1.05, 2)
        st.success(f"🧠 Estimated Auto fare range: ₹{low} – ₹{high}")

        # 🏆 Bonus feedback based on guess accuracy
        diff = abs(predicted_fare - guess)

        if diff <= 20:
            st.balloons()
            st.markdown("🎉 **Awesome guess! You're almost an Uber AI!** 😎")
        elif diff <= 50:
            st.markdown("✅ **Nice! That was pretty close.**")
        else:
            st.markdown("🤔 **Hmm, keep trying. Maybe check ride type or distance.**")
    else:
        st.warning("Please get a fare estimate first using the '🚕 Get Fare Estimate' button.")

# Simulate hourly fare trends
hours = list(range(24))
np.random.seed(42)

data = {
    'Hour': hours,
    'Moto': np.random.normal(loc=40, scale=5, size=24).round(2),
    'Auto': np.random.normal(loc=60, scale=8, size=24).round(2),
    'SUV': np.random.normal(loc=120, scale=15, size=24).round(2),
}

fare_df = pd.DataFrame(data)

st.subheader("📊 Uber Fare Trend by Hour")

melted_df = fare_df.melt(id_vars='Hour', var_name='Ride Type', value_name='Fare')

fig = px.line(
    melted_df,
    x='Hour',
    y='Fare',
    color='Ride Type',
    markers=True,
    title='Estimated Fare Trend by Hour',
    labels={'Hour': 'Hour of the Day', 'Fare': 'Estimated Fare (₹)'},
    template='plotly_dark'
)

st.plotly_chart(fig, use_container_width=True)

# ✅ Google Map
with col3:
    google_maps_url = f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAPS_API_KEY}&origin={pickup_lat},{pickup_lon}&destination={dropoff_lat},{dropoff_lon}"
    st.markdown(f'<iframe width="100%" height="600" src="{google_maps_url}" frameborder="0" style="border:0;" allowfullscreen=""></iframe>', unsafe_allow_html=True)
