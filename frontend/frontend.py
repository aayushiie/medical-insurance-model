import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Medical Insurance Category Predictor")

st.markdown("Enter your details below:")

age = st.number_input("Age", min_value=1, max_value=119, value=30)
gender = st.selectbox("Gender", options=['male', 'female', 'other'])
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
smokes = st.selectbox('Do you smoke?', options=['yes', 'no'])
region = st.selectbox('Region', options=['northeast', 'northwest', 'southeast', 'southwest'])
charges = st.number_input("Charges", min_value=0.0, value=1789.8)
monthly_premium_est = st.number_input("Monthly premium", min_value=0.0, value=1506.9)
charges_per_child = st.number_input("Charges per child", min_value=0.0, value=156.8)
bmi_age_interaction = st.number_input("BMI-Age Interaction", min_value=0.0, value=749.8)
risk_score = st.number_input("Risk score", min_value=0.0, max_value=9.0, value=5.45)
is_high_risk = st.selectbox("Are you at risk?", options=[True, False])
num_children = st.number_input("Number of children", min_value=0, value=1)

if st.button("Predict Insurance Category"):
    input_data = {
        'age': age,
        'gender': gender,
        'weight': weight,
        'height': height,
        'smokes': smokes,
        'region': region,
        'charges': charges,
        'monthly_premium_est': monthly_premium_est,
        'charges_per_child': charges_per_child,
        'bmi_age_interaction': bmi_age_interaction,
        'risk_score': risk_score,
        'is_high_risk': is_high_risk,
        'num_children': num_children
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code==200:
            result = response.json()
            st.success(f"Predicted medical insurance category: **{result['predicted_category']}**")
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server. Mkae sure it's running on port 8000.")

