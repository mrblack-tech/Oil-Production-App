import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# إعدادات الصفحة
st.set_page_config(page_title="Petro-Decision Support", layout="wide")

st.title("🚀 Smart Well Advisor & Artificial Lift Selector")
st.markdown("---")

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.header("1. Production Data")
q_i = st.sidebar.number_input("Initial Oil Rate (bbl/d)", value=1000)
d_i = st.sidebar.slider("Decline Rate (per year)", 0.1, 0.9, 0.2)
b = st.sidebar.slider("b-factor", 0.0, 1.0, 0.5)
months = st.sidebar.slider("Forecast Period", 12, 120, 60)

st.sidebar.header("2. Reservoir & Fluid")
water_cut = st.sidebar.slider("Current Water Cut (%)", 0, 95, 40)
bhp = st.sidebar.number_input("Bottomhole Pressure (psi)", value=2500)
gas_oil_ratio = st.sidebar.number_input("GOR (scf/bbl)", value=500)

# --- الحسابات الهندسية ---
time = np.arange(0, months + 1)
if b == 0:
    q_t = q_i * np.exp(-d_i * time / 12)
else:
    q_t = q_i / (1 + b * (d_i / 12) * time)**(1/b)

eur = (q_t.sum() / len(q_t)) * months * 30.44

# --- نظام التوصية الذكي (Logic) ---
st.subheader("💡 Engineering Recommendation")
rec_col1, rec_col2 = st.columns([1, 2])

with rec_col1:
    if water_cut > 70 and q_i > 500:
        recommendation = "Electrical Submersible Pump (ESP)"
        reason = "High fluid volume and high water cut detected."
        color = "blue"
    elif gas_oil_ratio > 800:
        recommendation = "Gas Lift System"
        reason = "High GOR makes the well a good candidate for gas injection."
        color = "green"
    elif q_i < 300:
        recommendation = "Sucker Rod Pump (SRP)"
        reason = "Low production rate; conventional pumping is more efficient."
        color = "orange"
    else:
        recommendation = "Natural Flow"
        reason = "Well conditions are stable for current production."
        color = "gray"
    
    st.info(f"**Suggested System:** {recommendation}")
    st.caption(f"Reason: {reason}")

# --- الرسم البياني المطور ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=q_t, name="Oil Rate", line=dict(color='#27ae60', width=4)))
fig.update_layout(title="Well Performance Analysis", xaxis_title="Months", yaxis_title="Rate (bbl/d)")
st.plotly_chart(fig, use_container_width=True)

# --- جدول البيانات وأزرار التحميل ---
with st.expander("View Detailed Calculations"):
    df = pd.DataFrame({"Month": time, "Rate": q_t.round(2)})
    st.dataframe(df, use_container_width=True)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    st.download_button("Download Full Report", output.getvalue(), "Well_Advisor_Report.xlsx")

st.markdown("---")
st.write("Constructed by Eng. Hussein | Technical Reference: API RP 11G")
