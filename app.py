import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات التصميم الاحترافي (UI Styles)
st.set_page_config(page_title="Petro-Elite Dashboard", layout="wide")

# تخصيص المظهر عبر CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e9ecef; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #004a99; color: white; }
    .sidebar .sidebar-content { background-image: linear-gradient(#2e3b4e, #1a2533); color: white; }
    h1 { color: #004a99; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# --- العنوان الرئيسي بشعار جذاب ---
st.title("💎 Petro-Optimizer Elite")
st.caption("Advanced Production Engineering & Economic Evaluation System")
st.markdown("---")

# 2. القائمة الجانبية المنظمة
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2967/2967232.png", width=80)
    st.header("Control Center")
    
    tab_eng, tab_econ = st.tabs(["⚙️ Engineering", "💰 Economics"])
    
    with tab_eng:
        p_res = st.number_input("Res. Pressure (psi)", value=3500)
        pi = st.slider("Productivity Index", 0.5, 5.0, 2.0)
        t_size = st.selectbox("Tubing Size", [2.375, 2.875, 3.5])
    
    with tab_econ:
        oil_price = st.slider("Oil Price ($/bbl)", 40, 120, 80)
        opex = st.number_input("Lifting Cost ($)", value=20)

# 3. محرك الحسابات
q_range = np.linspace(0, p_res * pi, 50)
pwf_ipr = p_res - (q_range / pi)
pwf_vlp = 200 + (0.0006 * q_range**2 / (t_size/2.875)**4) + 1200

idx = np.argwhere(np.diff(np.sign(pwf_ipr - pwf_vlp))).flatten()
opt_q = q_range[idx[0]] if len(idx) > 0 else 0
opt_p = pwf_ipr[idx[0]] if len(idx) > 0 else 0

# 4. لوحة النتائج (Dashboard Metrics)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Optimal Rate", f"{int(opt_q)} bbl/d", "Active")
with col_m2:
    st.metric("Flowing BHP", f"{int(opt_p)} psi", "-2%")
with col_m3:
    st.metric("Daily Profit", f"${int(opt_q*(oil_price-opex)):,}")
with col_m4:
    st.metric("Status", "Optimized", delta_color="normal")

st.markdown("### 📈 Technical Analysis")

# 5. الرسوم البيانية المنظمة
col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q_range, y=pwf_ipr, name="Reservoir (IPR)", line=dict(color='#004a99', width=4)))
    fig.add_trace(go.Scatter(x=q_range, y=pwf_vlp, name="Wellbore (VLP)", line=dict(color='#e63946', width=4)))
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=400)
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.write("**Quick Insights**")
    st.info(f"The well is currently operating at {int((opt_q/(p_res*pi))*100)}% of its potential AOF.")
    if opt_q > 500:
        st.success("✅ High Performance Well")
    else:
        st.warning("⚠️ Low Flow Optimization Needed")

# 6. تذييل الصفحة (Footer)
st.markdown("---")
f_col1, f_col2 = st.columns([4, 1])
f_col1.write(f"© 2026 Developed by Eng. Hussein Ali | Petroleum Systems Architect")
f_col2.download_button("📩 Export PDF Report", "Data", "Report.pdf")
