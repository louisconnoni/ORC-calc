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




# Convert heat loss percentage to fraction
LS = heat_loss_percent / 100.0

# Qevap calculation
Qevap = (1 - LS) * it_load_kw  # in kW

# Enthalpy calculations (in J/kg)
h1 = 226989.0315067
h2s = 0.1026089 * source_temp**2 - 3.3466673 * source_temp + 227006.0865709
h3 = -0.7999140 * source_temp**2 + 826.8497709 * source_temp + 402857.1775530
h4s = 0.6419351 * source_temp**2 + 93.0035927 * source_temp + 423522.4435321





# Convert efficiencies to fractions
PIE = pump_efficiency / 100.0
EIE = expander_efficiency / 100.0

# Specific Qevap (sp_Qevap), Work by Expander (sp_Wexpa), and Work by Pump (sp_Wpump)
sp_Qevap = h3 - (h1 - (h2s - h1) / PIE)
sp_Wexpa = (h3 - h4s) * EIE
sp_Wpump = (h2s - h1) / PIE





# Thermal efficiency
eta = (sp_Wexpa - sp_Wpump) / sp_Qevap

# Mass flow rate (kg/s)
mdotr = Qevap / sp_Qevap * 1000  # Convert from kW to W

# Expander power output (kW)
Wexp = mdotr * sp_Wexpa / 1000  # Convert from W to kW

# Pump power input (kW)
Wp = mdotr * sp_Wpump / 1000  # Convert from W to kW

# Evaporator heat transfer area (m²)
HTA_evap = 0.1537409 * Qevap**1.0766492

# Condenser heat flow (kW)
Qcond = Qevap * (1 - eta)

# Condenser heat transfer area (m²)
HTA_cond = 0.2065152 * Qcond**1.0842556






import math

# --- 3a. Pump Cost ---
K_p = [3.4771, 0.1350, 0.1438]
Fbm_p = 5.535
Fbm0_p = 3.240
min_p, max_p = 1, 100
N_p = 0.7

if Wp >= min_p and Wp <= max_p:
    Cp0_p = 10**(K_p[0] + K_p[1]*math.log10(Wp) + K_p[2]*(math.log10(Wp))**2)
elif Wp < min_p:
    Cp0_min_p = 10**(K_p[0] + K_p[1]*math.log10(min_p) + K_p[2]*(math.log10(min_p))**2)
    Cp0_p = Cp0_min_p * (Wp / min_p)**N_p
else:
    Cp0_max_p = 10**(K_p[0] + K_p[1]*math.log10(max_p) + K_p[2]*(math.log10(max_p))**2)
    Cp0_p = Cp0_max_p * (Wp / max_p)**N_p

Cbm_p = Cp0_p * Fbm_p
Cbm0_p = Cp0_p * Fbm0_p

# --- 3b. Expander Cost ---
K_exp = [2.2476, 1.4965, -0.1618]
Fbm_exp = 11.6
Fbm0_exp = 1.0
min_exp, max_exp = 100, 1500
N_exp = 0.6

if Wexp >= min_exp and Wexp <= max_exp:
    Cp0_exp = 10**(K_exp[0] + K_exp[1]*math.log10(Wexp) + K_exp[2]*(math.log10(Wexp))**2)
elif Wexp < min_exp:
    Cp0_min_exp = 10**(K_exp[0] + K_exp[1]*math.log10(min_exp) + K_exp[2]*(math.log10(min_exp))**2)
    Cp0_exp = Cp0_min_exp * (Wexp / min_exp)**N_exp
else:
    Cp0_max_exp = 10**(K_exp[0] + K_exp[1]*math.log10(max_exp) + K_exp[2]*(math.log10(max_exp))**2)
    Cp0_exp = Cp0_max_exp * (Wexp / max_exp)**N_exp

Cbm_exp = Cp0_exp * Fbm_exp
Cbm0_exp = Cp0_exp * Fbm0_exp

# --- 3c. Heat Exchangers (Evaporator & Condenser) ---
K_ST = [4.3247, -0.3030, 0.1634]
Fbm_ST = 6.27
Fbm0_ST = 3.29
N_ev = N_co = 0.6
min_ev = min_co = 10
max_ev = max_co = 1000

# Evaporator
if HTA_evap >= min_ev and HTA_evap <= max_ev:
    Cp0_ev = 10**(K_ST[0] + K_ST[1]*math.log10(HTA_evap) + K_ST[2]*(math.log10(HTA_evap))**2)
elif HTA_evap < min_ev:
    Cp0_min_ev = 10**(K_ST[0] + K_ST[1]*math.log10(min_ev) + K_ST[2]*(math.log10(min_ev))**2)
    Cp0_ev = Cp0_min_ev * (HTA_evap / min_ev)**N_ev
else:
    Cp0_max_ev = 10**(K_ST[0] + K_ST[1]*math.log10(max_ev) + K_ST[2]*(math.log10(max_ev))**2)
    Cp0_ev = Cp0_max_ev * (HTA_evap / max_ev)**N_ev

Cbm_ev = Cp0_ev * Fbm_ST
Cbm0_ev = Cp0_ev * Fbm0_ST

# Condenser
if HTA_cond >= min_co and HTA_cond <= max_co:
    Cp0_co = 10**(K_ST[0] + K_ST[1]*math.log10(HTA_cond) + K_ST[2]*(math.log10(HTA_cond))**2)
elif HTA_cond < min_co:
    Cp0_min_co = 10**(K_ST[0] + K_ST[1]*math.log10(min_co) + K_ST[2]*(math.log10(min_co))**2)
    Cp0_co = Cp0_min_co * (HTA_cond / min_co)**N_co
else:
    Cp0_max_co = 10**(K_ST[0] + K_ST[1]*math.log10(max_co) + K_ST[2]*(math.log10(max_co))**2)
    Cp0_co = Cp0_max_co * (HTA_cond / max_co)**N_co

Cbm_co = Cp0_co * Fbm_ST
Cbm0_co = Cp0_co * Fbm0_ST

# --- 3d. Generator ---
Cp0_gen = 2447 * (Wexp**0.49)
Fbm_gen = 3.5
Fbm0_gen = 1.0
Cbm_gen = Cp0_gen * Fbm_gen
Cbm0_gen = Cp0_gen * Fbm0_gen

# --- 3e. Working Fluid ---
Crpkg = 12.4  # $/kg
Cp0_r = 300 * mdotr * Crpkg

# --- 3f. Total Cost Calculations ---
Cbm0sum = Cbm0_p + Cbm0_exp + Cbm0_ev + Cbm0_co + Cbm0_gen + Cp0_r
Cbmsum = Cbm_p + Cbm_exp + Cbm_ev + Cbm_co + Cbm_gen
Ctm = Cbmsum * 1.18
Cgr = Ctm + 0.5 * Cbm0sum

CEPCI_2009 = 521.9
CEPCI_2018 = 567.5
Ctotal = Cgr * (CEPCI_2018 / CEPCI_2009)

UI = round(Ctotal, 3 - int(math.floor(math.log10(abs(Ctotal)))) - 1)

# --- Payback Period ---
EL = power_loss_percent / 100.0
EC = electricity_cost  # ¢/kWh
top = 1  # operating time in years
annual_savings = (EC / 100.0) * 24 * 365 * (1 - EL) * (Wexp - Wp)
PB = Ctotal / annual_savings if annual_savings > 0 else 0

# Carbon Emission Factors by state (kg CO2e/kWh)
state_cef = {
    'AL': 0.409, 'AK': 0.418, 'AZ': 0.388, 'AR': 0.485, 'CA': 0.256, 'CO': 0.563,
    'CT': 0.254, 'DE': 0.504, 'FL': 0.482, 'GA': 0.442, 'HI': 0.629, 'ID': 0.122,
    'IL': 0.309, 'IN': 0.707, 'IA': 0.403, 'KS': 0.425, 'KY': 0.750, 'LA': 0.421,
    'ME': 0.228, 'MD': 0.386, 'MA': 0.383, 'MI': 0.443, 'MN': 0.409, 'MS': 0.473,
    'MO': 0.671, 'MT': 0.452, 'NE': 0.501, 'NV': 0.442, 'NH': 0.167, 'NJ': 0.296,
    'NM': 0.608, 'NY': 0.230, 'NC': 0.396, 'ND': 0.595, 'OH': 0.607, 'OK': 0.431,
    'OR': 0.169, 'PA': 0.372, 'RI': 0.478, 'SC': 0.271, 'SD': 0.201, 'TN': 0.395,
    'TX': 0.468, 'UT': 0.685, 'VT': 0.075, 'VA': 0.379, 'WA': 0.101, 'WV': 0.788,
    'WI': 0.551, 'WY': 0.723
}

# Get CEF for selected location
CEF = state_cef.get(location, 0.372)  # Default to PA if not found

# Energy savings (kW)
ES = (1 - 0.01 * EL) * Wexp

# Carbon savings (metric tons CO2e/year)
CA = round(ES * CEF * 24 * 365 * 0.001, 3 - int(math.floor(math.log10(abs(ES * CEF * 24 * 365 * 0.001)))) - 1)


# --- Output Section ---
st.header("Results")

# --- Output Section ---
st.header("Results")

st.write(f"💰 **Payback Period (years):** {PB:.2f}")
st.write(f"💵 **Initial Investment:** ${UI:,.2f}")
st.write(f"⚡ **Energy Savings (kW):** {ES:,.2f}")
st.write(f"🌍 **Carbon Savings (Metric Tons CO₂/year):** {CA:,.2f}")

