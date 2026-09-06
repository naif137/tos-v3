import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="TOS V3 - Trading Operating System", layout="wide", page_icon="📈")

st.markdown("""
    <style>
    .main { background-color: #141619; color: #dcdcdc; }
    h1, h2, h3 { color: #00d296; }
    .stButton>button { background-color: #2d5aid; color: white; border-radius: 5px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 TOS V3: Smart Trading Operating System")
st.markdown("Professional Trading Journal & Risk Engine")

st.sidebar.header("📊 Account Settings")
capital = st.sidebar.number_input("Starting Capital ($)", value=100000.0, step=1000.0)
risk_pct = st.sidebar.slider("Risk Per Trade (%)", min_value=0.1, max_value=5.0, value=0.5) / 100.0

st.subheader("🎯 Pre-Trade Risk Terminal")
col1, col2, col3 = st.columns(3)

with col1:
    asset = st.text_input("Asset / Ticker", value="AAPL")
    planned_entry = st.number_input("Planned Entry", value=180.0)

with col2:
    stop_loss = st.number_input("Stop Loss", value=177.5)
    take_profit = st.number_input("Take Profit", value=187.5)

with col3:
    st.markdown("### Risk Analysis")
    risk_amount = capital * risk_pct
    price_diff = abs(planned_entry - stop_loss)
    reward_diff = abs(take_profit - planned_entry)
    
    rr_ratio = reward_diff / price_diff if price_diff > 0 else 0
    position_size = int(risk_amount / price_diff) if price_diff > 0 else 0
    
    st.metric(label="Risk / Reward (R:R)", value=f"{rr_ratio:.2f}")
    st.metric(label="Required Position Size", value=f"{position_size} Shares")

if rr_ratio < 1.5:
    st.error("🚨 HARD STOP: Poor R:R ratio (< 1.5), Trade Rejected!")
else:
    st.success("🟢 APPROVED: Trade meets risk parameters!")

st.markdown("---")
st.subheader("📓 Trade Journal & Behavior Engine")

if "journal_data" not in st.session_state:
    st.session_state.journal_data = pd.DataFrame(columns=[
        "Date", "Asset", "Actual Size", "Entry Price", "P&L ($)", "Behavioral Status"
    ])

with st.form("trade_form"):
    c1, c2, c3, c4, c5 = st.columns(5)
    t_date = c1.date_input("Date", datetime.date.today())
    t_asset = c2.text_input("Asset", "AAPL")
    t_size = c3.number_input("Actual Size", value=position_size)
    t_entry = c4.number_input("Actual Entry", value=180.0)
    t_pnl = c5.number_input("P&L ($)", value=350.0)
    
    submit_btn = st.form_submit_button("Record Trade in System")
    if submit_btn:
        status = "Disciplined" if t_size <= position_size else "Over-sized"
        new_row = {"Date": t_date, "Asset": t_asset, "Actual Size": t_size, "Entry Price": t_entry, "P&L ($)": t_pnl, "Behavioral Status": status}
        st.session_state.journal_data = pd.concat([st.session_state.journal_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Trade recorded successfully!")

if not st.session_state.journal_data.empty:
    st.dataframe(st.session_state.journal_data, use_container_width=True)
