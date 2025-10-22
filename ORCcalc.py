# app.py

import streamlit as st

# --- State to Electricity Cost Mapping ---
state_order = [
    'CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA', 'IL', 'IN', 'MI', 'OH', 'WI',
    'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD', 'DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA',
    'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX', 'AZ', 'CO', 'ID', 'MT', 'NV',
    'NM', 'UT', 'WY', 'CA', 'OR', 'WA', 'AK', 'HI'
]

state_costs = [
    16.10, 12.14, 14.88, 14.75, 15.24, 14.61, 12.31, 14.76, 8.99, 8.87, 10.30, 11.02, 9.97, 11.08,
    9.62, 10.49, 10.58, 9.32, 8.98, 9.18, 9.58, 9.95, 9.61, 9.98, 10.76, 8.56, 10.49, 8.07, 9.57,
    11.62, 9.70, 10.30, 10.50, 8.44, 8.91, 7.97, 8.31, 10.58, 9.95, 8.02, 10.20, 7.98, 10.27, 8.74,
    9.75, 15.89, 8.88, 8.51, 19.46, 26.82
]

state_to_cost = dict(zip(state_order, state_costs))

# --- App Title ---
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

# Set default source temperature based on cooling technology
if cooling_tech == "Air":
    default_temp = 50
elif cooling_tech == "Water":
    default_temp = 65
elif cooling_tech == "Two-phase":
    default_temp = 80
else:
    default_temp = 50  # fallback

# Source Temperature (°C)
source_temp = st.number_input("Source Temperature (°C)", value=default_temp)

# Heat Loss Percentage
heat_loss_percent = st.number_input("Heat Loss (%)", min_value=0.0, max_value=100.0, value=0.0)

# Data Center Location (State)
location = st.selectbox("Data Center Location", options=state_order)

# Auto-fill electricity cost based on selected state
default_cost = state_to_cost.get(location, 10.0)
electricity_cost = st.number_input("Electricity Cost (¢/kWh)", min_value=0.0, value=default_cost)

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