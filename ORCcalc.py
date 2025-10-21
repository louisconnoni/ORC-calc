# app.py

import streamlit as st

# Set the title of the app
st.title("Data Center Payback Calculator")

# --- Sidebar Help Button ---
with st.sidebar:
    if st.button("Help"):
        st.info("This app calculates the payback period, energy savings, and carbon savings for data center cooling systems. Future updates will include step-by-step explanations and visualizations.")

# --- Input Section ---
st.header("Input Parameters")

# IT Load in kW
it_load_kw = st.number_input("IT Load (kW)", min_value=0, value=10000)

# Cooling Technology
cooling_tech = st.selectbox("Cooling Technology", options=["Air", "Water", "Two-phase"])

# Source Temperature (°C)
source_temp = st.number_input("Source Temperature (°C)", value=50)

# Heat Loss Percentage
heat_loss_percent = st.number_input("Heat Loss (%)", min_value=0.0, max_value=100.0, value=0.0)

# Data Center Location (State)
location = st.selectbox("Data Center Location", options=[
    "California", "Texas", "New York", "Florida", "Illinois", "Other"
])

# Electricity Cost (¢/kWh)
electricity_cost = st.number_input("Electricity Cost (¢/kWh)", min_value=0.0, value=10.0)

# Power Loss Percentage
power_loss_percent = st.number_input("Power Loss (%)", min_value=0.0, max_value=100.0, value=0.0)

# Pump Isentropic Efficiency (%)
pump_efficiency = st.number_input("Pump Isentropic Efficiency (%)", min_value=0.0, max_value=100.0, value=60.0)

# Expander Isentropic Efficiency (%)
expander_efficiency = st.number_input("Expander Isentropic Efficiency (%)", min_value=0.0, max_value=100.0, value=60.0)

# --- Output Section ---
st.header("Results")

# Placeholder outputs (to be calculated later)
st.write("💰 **Payback Period (years):** [To be calculated]")
st.write("💵 **Initial Investment:** [To be calculated]")
st.write("⚡ **Energy Savings (kW):** [To be calculated]")
st.write("🌍 **Carbon Savings (Megatons CO₂/year):** [To be calculated]")