import streamlit as st
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load the pre-trained MLP model
model = tf.keras.models.load_model('battery_prediction_model.h5')  # Replace with the path to your model

# Initialize Streamlit app
st.title("EV Battery Health and Performance Estimator")

# Allow user to set constants
FULL_BATTERY_VOLTAGE = st.number_input("Full Battery Voltage (V)", min_value=0.0, value=58.8, format="%.2f")
MINIMUM_BATTERY_VOLTAGE = st.number_input("Minimum Battery Voltage (V)", min_value=0.0, value=38.5, format="%.2f")
FULL_CHARGE_CAPACITY = st.number_input("Full Charge Battery Capacity (kWh)", min_value=0.0, value=3.183216, format="%.6f")
CHARGE_CURRENT_CAPACITY = st.number_input("Charge Current Capacity (Ah)", min_value=0.0, value=54.5, format="%.2f")
RANGE_CONSTANT = st.number_input("Range Constant (km)", min_value=0.0, value=150.0, format="%.2f")

# User inputs for Battery Pack Voltage, Battery Current, and Internal Resistance
voltage = st.number_input("Battery Pack Voltage (V)", min_value=0.0, format="%.2f")
current = st.number_input("Battery Current (A)", min_value=0.0, format="%.2f")
resistance = st.number_input("Internal Resistance (Ω)", min_value=0.0, format="%.9f")

# Check if all inputs are provided
if st.button("Predict"):
    # Process input and prepare it for prediction
    input_data = np.array([[voltage, current, resistance]])
    
    # Scale the input using the same method as during training
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(input_data)  # Make sure this uses the original scaler from training

    # Make predictions
    predictions = model.predict(input_data_scaled)
    soc_pred, soh_pred, duration_pred, speed_pred = predictions[0]

    # Calculations for correct values
    voc = voltage + (current * resistance)
    soc = 100 * (voc - MINIMUM_BATTERY_VOLTAGE) / (FULL_BATTERY_VOLTAGE - MINIMUM_BATTERY_VOLTAGE)
    available_energy = (soc / 100) * FULL_CHARGE_CAPACITY
    soh = 100 * available_energy / FULL_CHARGE_CAPACITY
    duration = CHARGE_CURRENT_CAPACITY / current
    speed = RANGE_CONSTANT / duration

    st.subheader("Predicted Values")
    st.write(f"SoC (%): {soc:.2f}")
    st.write(f"SoH (%): {soh:.2f}")
    st.write(f"Duration (hrs): {duration:.2f}")
    st.write(f"Speed (km/hr): {speed:.2f}")

# Instructions to run on a network
st.write("To access this app on another device, use the command below:")
st.code("streamlit run app.py --server.address 0.0.0.0 --server.port 8501", language="bash")
