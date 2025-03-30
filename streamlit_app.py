import streamlit as st
import requests
import datetime
import random
import pyperclip
import streamlit.components.v1 as components

# ✅ Set Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="Uber Fare Prediction", layout="wide")

# ✅ Set Background Image with a Full-Screen Effect
page_bg_img = """
<style>
html, body, [data-testid="stAppViewContainer"] {
    background: url("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Uber_logo_2018.svg/2560px-Uber_logo_2018.svg.png") no-repeat center center fixed;
    background-size: cover;
}

[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.6); /* Optional: Dark sidebar effect */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


# ✅ API Keys
GOOGLE_MAPS_API_KEY = "AIzaSyAbgA9gFMQo2ccFDTLS0L1oD3o48DQqZoo"
FASTAPI_URL = "https://fastapi-catboost-deployment.onrender.com/predict/"

# ✅ Location Mapping
location_mapping = {
    "Anna Nagar (VR Mall) 🏬": (13.0827, 80.2170, 1),
    "Chennai Central Railway Station (Chennai Central) 🚉": (13.0839, 80.2707, 2),
    "Guindy (Race Course) 🏇": (13.0072, 80.2209, 3),
    "Marina Beach (Marina Beach) 🌊": (13.0495, 80.2820, 4),
    "Perambur (Sri Brindavan Theatre) 🎭": (13.1173, 80.2503, 5),
    "Pallavaram (Pallavaram Market) 🛍️": (12.9687, 80.1481, 6),
    "Vadapalani (Vadapalani Murugan Temple) 🛕": (13.0503, 80.2127, 7),
    "Koyambedu (Koyambedu Market) 🍎": (13.0668, 80.1989, 8),
    "OMR (IT Corridor) 🏢": (12.9279, 80.1362, 9),
    "Ambattur (Industrial Estate) 🏭": (13.1146, 80.1580, 10),
    "Velachery (Phoenix Marketcity) 🛒": (12.9791, 80.2209, 11),
    "Porur (MIOT Hospital) 🏥": (13.0388, 80.1561, 12),
    "Sholinganallur (ECR Beach) 🏖️": (12.8996, 80.2273, 13),
    "Adyar (Adyar Bridge) 🌉": (13.0067, 80.2551, 14),
    "Chennai Airport (International Airport) ✈️": (12.9816, 80.1636, 15),
    "T Nagar (Pondy Bazaar) 🛍️": (13.0400, 80.2330, 16),
    "Tambaram (Railway Station) 🚂": (12.9250, 80.1273, 17),
    "Mylapore (Kapaleeshwarar Temple) 🛕": (13.0315, 80.2684, 18),
    "ECR (Long Drive) 🏎️": (12.9719, 80.1393, 19),
    "Medavakkam (Residential Area) 🏠": (12.9165, 80.1852, 20)
}

# ✅ Share Button at the Top
share_url = "https://your-streamlit-app-url.com"
col_title, col_share = st.columns([0.9, 0.1])

with col_title:
    st.markdown("<h1 style='text-align: center;'>🚖 Uber Fare Prediction</h1>", unsafe_allow_html=True)

with col_share:
    if st.button("🔗"):
        pyperclip.copy(share_url)
        st.success("Link copied to clipboard!")

st.write("Plan your next trip with the price estimator.")

# ✅ Layout: Inputs (Left), Ride Options (Middle), Google Maps (Right)
col1, col2, col3 = st.columns([2, 2, 2])  

with col1:
    pickup_location = st.selectbox("📍 Pickup Location", list(location_mapping.keys()), index=0)
    dropoff_location = st.selectbox("📍 Drop-off Location", list(location_mapping.keys()), index=1)
    pickup_date = st.date_input("📅 Select Pickup Date", datetime.date.today())

# Select time from current time to future in 12-hour format with AM/PM
    now = datetime.datetime.now()
    time_options = [now + datetime.timedelta(minutes=5 * i) for i in range(288)]
    time_labels = [t.strftime("%I:%M %p") for t in time_options]  # 12-hour format with AM/PM

    pickup_time = st.selectbox("⏰ Select Pickup Time", time_labels, index=0)

    # Convert selected time back to 24-hour format for processing
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

    if st.button("🚕 Get Fare Estimate"):
        data = {"features": features}
        response = requests.post(FASTAPI_URL, json=data)

        if response.status_code == 200:
            result = response.json()
            if "prediction" in result:
                base_fare = round(result["prediction"][0], 2)

                auto_fare = base_fare
                moto_fare = round(auto_fare * (0.65 + (random.uniform(0, 0.1))), 2)
                uber_fare = round(auto_fare * (1.35 + (random.uniform(0, 0.1))), 2)

                with col2:
                    st.markdown("### 🚘 Choose a ride")

                    st.markdown(f"""
                        <div style="border: 2px solid black; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                            <h3>🏍️ Moto</h3>
                            <p>Fast & affordable bike ride</p>
                            <h2>₹{moto_fare}</h2>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div style="border: 2px solid black; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                            <h3>🛺 Auto</h3>
                            <p>Affordable 3-seater ride</p>
                            <h2>₹{auto_fare}</h2>
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                        <div style="border: 2px solid black; padding: 10px; border-radius: 10px; margin-bottom: 10px;">
                            <h3>🚗 Uber Go</h3>
                            <p>Comfortable car ride for 4 people</p>
                            <h2>₹{uber_fare}</h2>
                        </div>
                    """, unsafe_allow_html=True)

            else:
                st.error(f"⚠️ Error in response: {result}")
        else:
            st.error(f"❌ API Request Failed! Status Code: {response.status_code}")

# ✅ Google Maps in the Right Column
with col3:
    google_maps_url = f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAPS_API_KEY}&origin={pickup_lat},{pickup_lon}&destination={dropoff_lat},{dropoff_lon}&mode=driving"

    components.html(f"""
        <iframe width="100%" height="540" style="border:0" loading="lazy"
            allowfullscreen src="{google_maps_url}">
        </iframe>
    """, height=540)
