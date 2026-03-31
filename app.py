import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات الصفحة والواجهة
st.set_config(page_title="Petro-Decision Support Pro", layout="wide")
st.title("🚀 Smart Well Advisor: Production, Economics & Lift Selection")
st.markdown("---")

# 2. القائمة الجانبية للمدخلات (Sidebar)
with st.sidebar:
    st.header("📥 Input Parameters")
    
    with st.expander("1. Reservoir & Engineering", expanded=True):
        q_i = st.number_input("Initial Oil Rate (bbl/d)", value=1000)
        d_i = st.slider("Decline Rate (per year)", 0.1, 0.9, 0.2)
        b = st.slider("b-factor (Arps)", 0.0, 1.0, 0.5)
        months = st.slider("Forecast Duration (Months)", 12, 120, 60)
    
    with st.expander("2. Fluid & Pressure", expanded=True):
        water_cut = st.slider("Water Cut (%)", 0, 95, 45)
        gor = st.number_input("Gas Oil Ratio (scf/bbl)", value=600)
        bhp = st.number_input("Bottomhole Pressure (psi)", value=2000)

    with st.expander("3. Economics", expanded=True):
        oil_price = st.slider("Oil Price ($/bbl)", 40, 150, 80)
        opex = st.number_input("Operating Cost ($/bbl)", value=25)

# 3. الحسابات الهندسية والمالية
time = np.arange(0, months + 1)
# معادلة Arps
if b == 0:
    q_t = q_i * np.exp(-d_i * time / 12)
else:
    q_t = q_i / (1 + b * (d_i / 12) * time)**(1/b)

# الإنتاج التراكمي المستقر
eur = (q_t.sum() / len(q_t)) * months * 30.44
net_profit_per_bbl = oil_price - opex
total_revenue = eur * net_profit_per_bbl
economic_limit_rate = 50 

# 4. نظام التوصية الذكي (Artificial Lift Selection Logic)
st.subheader("💡 Engineering Recommendation & Analysis")
rec_col1, rec_col2, rec_col3 = st.columns(3)

# منطق الاختيار
if water_cut > 75 and q_i > 500:
    lift_rec = "ESP (Electrical Submersible Pump)"
    color = "blue"
    reason = "Ideal for high fluid volumes and high water cut."
elif gor > 1000:
    lift_rec = "Gas Lift"
    color = "green"
    reason = "High GOR detected; gas injection will optimize flow."
elif q_i < 300 and bhp < 1000:
    lift_rec = "Sucker Rod Pump (SRP)"
    color = "orange"
    reason = "Low rate and low pressure; mechanical lift is best."
else:
    lift_rec = "Natural Flow / Monitoring"
    color = "gray"
    reason = "Conditions are stable for current production methods."

with rec_col1:
    st.metric("Total Recovery (EUR)", f"{int(eur):,} bbl")
with rec_col2:
    st.metric("Net Revenue", f"${int(total_revenue):,}")
with rec_col3:
    st.info(f"**Lift Rec:** {lift_rec}")
    st.caption(f"Reason: {reason}")

# 5. الرسم البياني التفاعلي
fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=q_t, name="Oil Rate", fill='tozeroy', line=dict(color='#27ae60', width=4)))
fig.add_hline(y=economic_limit_rate, line_dash="dot", line_color="red", annotation_text="Economic Limit")
fig.update_layout(title="Production Forecast & Economic Limit", xaxis_title="Months", yaxis_title="Rate (bbl/d)")
st.plotly_chart(fig, use_container_width=True)

# 6. تصدير البيانات والتقارير
with st.expander("📥 View Data & Download Reports"):
    df = pd.DataFrame({
        "Month": time,
        "Oil Rate (bbl/d)": q_t.round(2),
        "Revenue ($)": (q_t * 30.44 * net_profit_per_bbl).round(0)
    })
    st.dataframe(df, use_container_width=True)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Well_Analysis')
    
    st.download_button(
        label="Download Professional Excel Report",
        data=output.getvalue(),
        file_name='Engineering_Decision_Report.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

st.markdown("---")
st.write(f"Prepared by: Eng. Hussein | {months} Month Analysis | Final Profitability: {'Yes' if q_t[-1] > economic_limit_rate else 'Action Required'}")
