import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Page Configuration
st.set_page_config(page_title="PetroDigital - Well Analytics", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛢️ Advanced Well Analytics & Water Cut Forecasting")
st.markdown("---")

# Sidebar - Engineering Inputs
with st.sidebar:
    st.header("⚙️ Engineering Parameters")
    
    with st.expander("1. Decline Curve (Arps)", expanded=True):
        qi = st.number_input("Initial Oil Rate (qi) [bbl/d]", value=1200)
        di = st.slider("Nominal Decline Rate (Di)", 0.01, 0.30, 0.08)
        b_factor = st.slider("Arps b-factor", 0.0, 1.0, 0.5)
    
    with st.expander("2. Water Cut Model", expanded=True):
        initial_wc = st.slider("Initial Water Cut (%)", 5, 50, 10)
        wc_growth = st.slider("Water Growth Factor", 0.001, 0.050, 0.015, format="%.3f")
    
    forecast_months = st.number_input("Forecast Duration (Months)", value=48)

# Engineering Logic / Functions
def calculate_production(t, qi, di, b):
    # Arps Hyperbolic/Exponential/Harmonic
    if b == 0:
        return qi * np.exp(-di * t)
    return qi / (1 + b * di * t)**(1/b)

def calculate_water_cut(cum_oil, init_wc, growth):
    # Simplified Water Drive Model: WC = 1 - (1-init_wc)*exp(-growth * cum_oil/1000)
    # This simulates how water increases as we deplete the reservoir
    wc = 100 - (100 - init_wc) * np.exp(-growth * cum_oil / 5000)
    return np.clip(wc, init_wc, 99.0)

# Data Generation
months = np.arange(0, forecast_months + 1)
oil_rates = calculate_production(months, qi, di, b_factor)
cum_oil = np.cumsum(oil_rates * 30.44) # Cumulative Oil in bbls

water_cuts = [calculate_water_cut(c, initial_wc, wc_growth) for c in cum_oil]
water_rates = oil_rates * (np.array(water_cuts) / (100 - np.array(water_cuts)))

# Analysis Metrics
total_oil = cum_oil[-1]
final_wc = water_cuts[-1]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Oil Recovery (EUR)", f"{int(total_oil):,} bbl")
col2.metric("Final Water Cut", f"{final_wc:.1f}%")
col3.metric("Avg Oil Rate", f"{int(np.mean(oil_rates))} bbl/d")
col4.metric("Water/Oil Ratio (Final)", f"{(final_wc/(100-final_wc)):.2f}")

# Main Visualizations
st.markdown("### 📈 Production Performance & Water Evolution")
fig, ax1 = plt.subplots(figsize=(12, 5))

# Plot Oil Rate
color = 'tab:green'
ax1.set_xlabel('Time (Months)', fontsize=12)
ax1.set_ylabel('Oil Rate (bbl/d)', color=color, fontsize=12)
ax1.plot(months, oil_rates, color=color, linewidth=3, label='Oil Production')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, alpha=0.3)

# Create second axis for Water Cut
ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Water Cut (%)', color=color, fontsize=12)
ax2.plot(months, water_cuts, color=color, linestyle='--', linewidth=2, label='Water Cut %')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_ylim(0, 100)

fig.tight_layout()
st.pyplot(fig)

# Economic Warning Alert
if final_wc > 85:
    st.warning(f"⚠️ High Water Cut Alert: Well reaching economic limit at month {forecast_months}. Consider Artificial Lift or Water Shut-off.")

# Data Table
with st.expander("View Raw Calculation Data"):
    df = pd.DataFrame({
        "Month": months,
        "Oil Rate (bbl/d)": oil_rates.astype(int),
        "Water Rate (bbl/d)": water_rates.astype(int),
        "Water Cut (%)": np.round(water_cuts, 2),
        "Cumulative Oil (bbl)": cum_oil.astype(int)
    })
    st.dataframe(df, use_container_width=True)
    
st.caption("Engineered by Hussein | Reference: SPE-PRMS Guidelines for Reserve Estimation")
