import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات الصفحة (وضوح عالٍ وبساطة)
st.set_page_config(page_title="Petro-Elite Dashboard", layout="wide")

# تنسيق بسيط لضمان وضوح النصوص والأرقام
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    div[data-testid="stMetric"] { background-color: #ffffff; border: 1px solid #e2e8f0; padding: 15px; border-radius: 10px; }
    h1, h2, h3 { color: #0f172a; }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (Control Center)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>Control Center</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 0.9em; color: #64748b;'>Developed & Executed by:<br><b>Eng. Hussein Al-Ameri</b></p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # مدخلات المهندس الأساسية (Arps Decline Parameters)
    st.subheader("📥 Input Parameters")
    q_i = st.number_input("Initial Rate (bbl/d)", value=1000)
    d_i = st.slider("Decline Rate (D)", 0.1, 0.9, 0.2)
    b = st.slider("b-factor", 0.0, 1.0, 0.5)
    months = st.slider("Forecast Period (Months)", 12, 120, 48)
    
    st.markdown("---")
    st.subheader("💰 Economics")
    oil_price = st.number_input("Oil Price ($/bbl)", value=80)
    water_cut = st.slider("Water Cut (%)", 0, 100, 45)

# 3. الحسابات الهندسية (Decline Curve Analysis)
time = np.arange(0, months + 1)
# معادلة Arps الشهيرة للإنتاج
if b == 0:
    q_t = q_i * np.exp(-d_i * time / 12)
else:
    q_t = q_i / (1 + b * (d_i / 12) * time)**(1/b)

# حساب إجمالي الإنتاج المتوقع (EUR)
eur = (q_t.sum() / len(q_t)) * months * 30.44

# 4. واجهة النتائج الرئيسية
st.title("💎 Petro-Elite™ Production Optimizer")
st.write("Professional Decision Support System for Petroleum Engineers")
st.markdown("---")

# عرض المؤشرات الرئيسية (Metrics)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Recovery (EUR)", f"{int(eur):,} bbl")
with col2:
    st.metric("Daily Revenue", f"${int(q_t[0] * oil_price):,}")
with col3:
    # نظام ترشيح الرفع الاصطناعي بناءً على المعطيات
    if water_cut > 75:
        lift = "ESP Recommended"
    elif q_i < 300:
        lift = "SRP Recommended"
    else:
        lift = "Natural Flow"
    st.info(f"**Status:** {lift}")

# 5. الرسم البياني (Production Forecast Chart)
st.subheader("📊 Production Decline Forecast")
fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=q_t, name="Oil Rate", line=dict(color='#0284c7', width=4), fill='tozeroy'))
fig.update_layout(
    plot_bgcolor='white',
    xaxis_title="Time (Months)",
    yaxis_title="Oil Rate (bbl/d)",
    height=500,
    margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig, use_container_width=True)

# 6. تذييل الصفحة والبيانات
with st.expander("📥 Export Raw Data"):
    df = pd.DataFrame({"Month": time, "Predicted Rate": q_t.round(2)})
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV Report", csv, "Production_Report.csv", "text/csv")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94a3b8;'>© 2026 | Petroleum Engineering Excellence | Hadramout, Yemen</p>", unsafe_allow_html=True)
