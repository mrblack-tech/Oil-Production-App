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
    
    /* تنسيق خاص لتوسيط الشعار */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- العنوان الرئيسي بشعار جذاب ---
st.title("💎 Petro-Optimizer Elite")
st.caption("Advanced Production Engineering & Economic Evaluation System")
st.markdown("---")

# 2. القائمة الجانبية المنظمة (المكان الجديد للشعار)
with st.sidebar:
    # --- إضافة الشعار هنا ---
    # يمكنك استبدال هذا الرابط برابط شعارك الخاص إذا كان مرفوعاً على الإنترنت
    logo_url = "https://cdn-icons-png.flaticon.com/512/2967/2967232.png" 
    st.markdown(f'<div class="logo-container"><img src="{logo_url}" width="120"></div>', unsafe_allow_html=True)
    
    st.header("Asset Control Center")
    st.markdown("Developed by: Eng. Hussein Ali")
    
    tab_eng, tab_econ = st.tabs(["⚙️ Engineering", "💰 Economics"])
    
    with tab_eng:
        p_res = st.number_input("Res. Pressure (psi)", value=3500)
        pi = st.slider("Productivity Index", 0.5, 5.0, 2.0)
        t_size = st.selectbox("Tubing Size", [2.375, 2.875, 3.5])
    
    with tab_econ:
        oil_price = st.slider("Oil Price ($/bbl)", 40, 120, 80)
        opex = st.number_input("Lifting Cost ($)", value=20)

# 3. محرك الحسابات (Node Analysis)
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
    st.metric("Flowing BHP", f"{int(opt_p)} psi")
with col_m3:
    st.metric("Daily Profit", f"${int(opt_q*(oil_price-opex)):,}")
with col_m4:
    st.metric("Status", "Optimized")

st.markdown("### 📈 Technical Analysis")

# 5. الرسوم البيانية المنظمة
col_chart1, col_chart2 = st.columns([2, 1])

with col_chart1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=q_range, y=pwf_ipr, name="Reservoir (IPR)", line=dict(color='#004a99', width=4)))
    fig.add_trace(go.Scatter(x=q_range, y=pwf_vlp, name="Wellbore (VLP)", line=dict(color='#e63946', width=4)))
    
    if opt_q > 0:
        fig.add_trace(go.Scatter(x=[opt_q], y=[opt_p], mode='markers+text', 
                                 name="Match Point", text=["MATCH"], 
                                 marker=dict(size=12, color='gold', symbol='star')))
        
    fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=400,
                      xaxis_title="Rate (bbl/d)", yaxis_title="Pressure (psi)")
    st.plotly_chart(fig, use_container_width=True)

with col_chart2:
    st.write("**Smart Insights**")
    st.info(f"The well is currently operating at {int((opt_q/(p_res*pi))*100)}% of its theoretical AOF.")
    if opt_q > 500:
        st.success("✅ High Performance Asset")
    else:
        st.warning("⚠️ Optimization Candidate")

# 6. تذييل الصفحة (Footer)
st.markdown("---")
f_col1, f_col2 = st.columns([4, 1])
f_col1.write(f"© 2026 Petro-Elite™ | Strategic Asset Management Tool | اليمن")

# ميزة إضافية: تحميل ملف البيانات (الجدول) كـ CSV
output = BytesIO()
df = pd.DataFrame({"Month": np.arange(0, 13), "Oil Rate": np.ones(13)*opt_q})
df.to_csv(output, index=False)
f_col2.download_button("📩 Download Data", output.getvalue(), "Well_Data.csv")
