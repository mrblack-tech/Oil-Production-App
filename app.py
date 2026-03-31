import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات بسيطة وواضحة (بدون تعقيدات CSS)
st.set_page_config(page_title="Petro-Elite Dashboard", layout="wide")

# 2. القائمة الجانبية (الشعار + المدخلات الأساسية فقط)
with st.sidebar:
    # شعار برج الحفر وقطرة النفط
    logo_url = "https://cdn-icons-png.flaticon.com/512/3011/3011503.png"
    st.image(logo_url, width=120)
    
    st.header("Control Center")
    st.write(f"Eng. Hussein Ali")
    st.markdown("---")
    
    # المدخلات كما في المراحل السابقة
    q_i = st.number_input("Initial Oil Rate (bbl/d)", value=1000)
    d_i = st.slider("Decline Rate", 0.1, 0.9, 0.2)
    b = st.slider("b-factor", 0.0, 1.0, 0.5)
    months = st.slider("Forecast Months", 12, 72, 36)
    
    st.markdown("---")
    water_cut = st.slider("Water Cut (%)", 0, 100, 40)
    oil_price = st.number_input("Oil Price ($/bbl)", value=80)

# 3. الحسابات الهندسية (المرحلة الثالثة)
time = np.arange(0, months + 1)
if b == 0:
    q_t = q_i * np.exp(-d_i * time / 12)
else:
    q_t = q_i / (1 + b * (d_i / 12) * time)**(1/b)

eur = (q_t.sum() / len(q_t)) * months * 30.44

# 4. واجهة النتائج (مرتبة وبسيطة)
st.title("🚀 Petro-Elite Dashboard")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Total Recovery (EUR)", f"{int(eur):,} bbl")
col2.metric("Final Rate", f"{int(q_t[-1])} bbl/d")

# منطق التوصية الذكي (المرحلة 3)
if water_cut > 70:
    recommendation = "ESP (High Water Cut)"
elif q_i < 300:
    recommendation = "Sucker Rod Pump"
else:
    recommendation = "Natural Flow"
col3.info(f"**Recommended:** {recommendation}")

# 5. الرسم البياني (واضح وعريض)
fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=q_t, name="Oil Production", line=dict(color='blue', width=3)))
fig.update_layout(title="Well Performance Forecast", xaxis_title="Months", yaxis_title="Rate (bbl/d)", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# 6. الجدول والتحميل
with st.expander("View Data Table"):
    df = pd.DataFrame({"Month": time, "Rate": q_t.round(2)})
    st.dataframe(df, use_container_width=True)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    st.download_button("Download Excel Report", output.getvalue(), "Production_Report.xlsx")

st.markdown("---")
st.write("Prepared by Eng. Hussein Ali | Petroleum Engineering Excellence")
