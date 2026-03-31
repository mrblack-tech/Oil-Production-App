import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات الصفحة الاحترافية (Page Config)
st.set_page_config(page_title="Petro-Elite Dashboard", layout="wide", page_icon="🛢️")

# تحسين المظهر البصري ليكون مشرقاً وعالي الوضوح
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    div[data-testid="stMetric"] { background-color: #fdfdfd; border: 1px solid #edf2f7; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #1e293b; font-family: 'Inter', sans-serif; }
    .logo-box { display: flex; justify-content: center; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (الشعار الصناعي + التحكم)
with st.sidebar:
    # شعار برج الحفر وقطرة النفط
    logo_url = "https://cdn-icons-png.flaticon.com/512/3011/3011503.png"
    st.markdown(f'<div class="logo-box"><img src="{logo_url}" width="120"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Eng. Hussein Ali</h3>", unsafe_allow_html=True)
    st.write("---")
    
    st.subheader("🛠️ Reservoir & Tubing")
    p_res = st.number_input("Res. Pressure (psi)", value=3500)
    pi = st.slider("Productivity Index", 0.5, 5.0, 1.5)
    t_size = st.selectbox("Tubing Size (in)", [2.375, 2.875, 3.5])
    
    st.subheader("💰 Economics")
    oil_price = st.slider("Oil Price ($/bbl)", 40, 140, 85)

# 3. محرك الحسابات المتقدم (Nodal Analysis Logic)
q_range = np.linspace(0, p_res * pi, 100)
pwf_ipr = p_res - (q_range / pi)
# معادلة VLP فيزيائية محسنة
pwf_vlp = 250 + (0.0008 * q_range**1.85 / (t_size/2.875)**4) + 1150

idx = np.argwhere(np.diff(np.sign(pwf_ipr - pwf_vlp))).flatten()
opt_q = q_range[idx[0]] if len(idx) > 0 else 0
opt_p = pwf_ipr[idx[0]] if len(idx) > 0 else 0

# 4. لوحة النتائج الرئيسية
st.title("💎 Petro-Elite™ Production Optimizer")
st.caption("Strategic Decision Support for Oil & Gas Assets")

c1, c2, c3 = st.columns(3)
c1.metric("Optimal Rate", f"{int(opt_q)} bbl/d")
c2.metric("Flowing Pressure", f"{int(opt_p)} psi")
c3.metric("Daily Gross Revenue", f"${int(opt_q * oil_price):,}")

# 5. الرسم البياني التفاعلي
st.markdown("### 📊 Nodal Analysis: Performance Match")
fig = go.Figure()
fig.add_trace(go.Scatter(x=q_range, y=pwf_ipr, name="IPR Curve", line=dict(color='#2563eb', width=4)))
fig.add_trace(go.Scatter(x=q_range, y=pwf_vlp, name="VLP Curve", line=dict(color='#dc2626', width=4)))

if opt_q > 0:
    fig.add_trace(go.Scatter(x=[opt_q], y=[opt_p], mode='markers+text', 
                             name="Match Point", text=["OPTIMAL"], 
                             marker=dict(size=15, color='#fbbf24', symbol='diamond')))

fig.update_layout(plot_bgcolor='white', xaxis_title="Rate (bbl/d)", yaxis_title="Pressure (psi)",
                  height=500, margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# 6. التذييل والتحميل
st.markdown("---")
col_f1, col_f2 = st.columns([4, 1])
col_f1.write("© 2026 Developed by Eng. Hussein Ali Al-Amery | Petroleum Engineering")

# زر تحميل البيانات
df_final = pd.DataFrame({"Rate": q_range, "IPR": pwf_ipr, "VLP": pwf_vlp})
csv = df_final.to_csv(index=False).encode('utf-8')
col_f2.download_button("📩 Download Data", csv, "well_data.csv", "text/csv")
