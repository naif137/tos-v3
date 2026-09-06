import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="TOS V3 - Trading Operating System", layout="wide", page_icon="📈")

# --- الإعدادات الجانبية (اللغة والسوق) ---
st.sidebar.header("⚙️ Settings | الإعدادات")
lang = st.sidebar.radio("Language / اللغة", ["عربي", "English"])
market = st.sidebar.selectbox("Market / السوق" if lang == "English" else "السوق", 
                              ["US Market", "Saudi Market"] if lang == "English" else ["السوق الأمريكي", "السوق السعودي"])

currency = "$" if "US" in market or "الأمريكي" in market else "SAR"
default_ticker = "AAPL" if "US" in market or "الأمريكي" in market else "2222.SR"

# --- القاموس (عربي/إنجليزي) ---
t = {
    "title": "🚀 TOS V3: Smart Trading Operating System" if lang == "English" else "🚀 نظام التداول الذكي TOS V3",
    "subtitle": "Professional Trading Journal & Risk Engine" if lang == "English" else "سجل التداول الاحترافي ومحرك إدارة المخاطر",
    "account_settings": "📊 Account Settings" if lang == "English" else "📊 إعدادات الحساب",
    "capital": "Starting Capital" if lang == "English" else "رأس المال الأساسي",
    "risk_pct": "Risk Per Trade (%)" if lang == "English" else "نسبة المخاطرة لكل صفقة (%)",
    "risk_terminal": "🎯 Pre-Trade Risk Terminal" if lang == "English" else "🎯 منصة المخاطر قبل الصفقة",
    "asset": "Asset / Ticker" if lang == "English" else "الرمز / السهم",
    "entry": "Planned Entry" if lang == "English" else "سعر الدخول المستهدف",
    "sl": "Stop Loss" if lang == "English" else "وقف الخسارة",
    "tp": "Take Profit" if lang == "English" else "جني الأرباح",
    "risk_analysis": "### Risk Analysis" if lang == "English" else "### تحليل المخاطر",
    "rr": "Risk / Reward (R:R)" if lang == "English" else "العائد للمخاطرة (R:R)",
    "pos_size": "Required Position Size" if lang == "English" else "حجم المركز المطلوب (أسهم/عقود)",
    "hard_stop": "🚨 HARD STOP: Poor R:R ratio (< 1.5), Trade Rejected!" if lang == "English" else "🚨 توقف إجباري: نسبة العائد للمخاطرة ضعيفة (< 1.5)، الصفقة مرفوضة!",
    "approved": "🟢 APPROVED: Trade meets risk parameters!" if lang == "English" else "🟢 مسموح: الصفقة تتوافق مع معايير المخاطرة!",
    "journal_title": "📓 Trade Journal & Behavior Engine" if lang == "English" else "📓 سجل الصفقات ومحرك السلوكيات",
    "date": "Date" if lang == "English" else "التاريخ",
    "actual_size": "Actual Size" if lang == "English" else "الكمية الفعلية",
    "actual_entry": "Actual Entry" if lang == "English" else "سعر الدخول الفعلي",
    "pnl": "P&L" if lang == "English" else "الربح/الخسارة",
    "record_btn": "Record Trade in System" if lang == "English" else "تسجيل الصفقة في النظام",
    "success": "Trade recorded successfully!" if lang == "English" else "تم تسجيل الصفقة بنجاح!",
    "disciplined": "Disciplined" if lang == "English" else "منضبط",
    "oversized": "Over-sized" if lang == "English" else "كمية زائدة"
}

# --- تنسيق التصميم واتجاه الشاشة ---
if lang == "عربي":
    st.markdown("""<style>
        .main, .stMarkdown, .stText, [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        .main { background-color: #141619; color: #dcdcdc; }
        h1, h2, h3 { color: #00d296; }
        .stButton>button { background-color: #2d5aid; color: white; border-radius: 5px; width: 100%; }
        </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
        .main { background-color: #141619; color: #dcdcdc; }
        h1, h2, h3 { color: #00d296; }
        .stButton>button { background-color: #2d5aid; color: white; border-radius: 5px; width: 100%; }
        </style>""", unsafe_allow_html=True)

# --- واجهة التطبيق الرئيسية ---
st.title(t["title"])
st.markdown(t["subtitle"])

st.sidebar.header(t["account_settings"])
capital = st.sidebar.number_input(f'{t["capital"]} ({currency})', value=100000.0, step=1000.0)
risk_pct = st.sidebar.slider(t["risk_pct"], min_value=0.1, max_value=5.0, value=0.5) / 100.0

st.subheader(t["risk_terminal"])
col1, col2, col3 = st.columns(3)

with col1:
    asset = st.text_input(t["asset"], value=default_ticker)
    planned_entry = st.number_input(t["entry"], value=180.0)

with col2:
    stop_loss = st.number_input(t["sl"], value=177.5)
    take_profit = st.number_input(t["tp"], value=187.5)

with col3:
    st.markdown(t["risk_analysis"])
    risk_amount = capital * risk_pct
    price_diff = abs(planned_entry - stop_loss)
    reward_diff = abs(take_profit - planned_entry)
    
    rr_ratio = reward_diff / price_diff if price_diff > 0 else 0
    position_size = int(risk_amount / price_diff) if price_diff > 0 else 0
    
    st.metric(label=t["rr"], value=f"{rr_ratio:.2f}")
    st.metric(label=t["pos_size"], value=f"{position_size}")

if rr_ratio < 1.5:
    st.error(t["hard_stop"])
else:
    st.success(t["approved"])

st.markdown("---")
st.subheader(t["journal_title"])

if "journal_data" not in st.session_state:
    st.session_state.journal_data = pd.DataFrame(columns=[
        "Date", "Asset", "Actual Size", "Entry Price", f'P&L ({currency})', "Status"
    ])

with st.form("trade_form"):
    c1, c2, c3, c4, c5 = st.columns(5)
    t_date = c1.date_input(t["date"], datetime.date.today())
    t_asset = c2.text_input(t["asset"], asset)
    t_size = c3.number_input(t["actual_size"], value=position_size)
    t_entry = c4.number_input(t["actual_entry"], value=planned_entry)
    t_pnl = c5.number_input(f'{t["pnl"]} ({currency})', value=0.0)
    
    submit_btn = st.form_submit_button(t["record_btn"])
    if submit_btn:
        status = t["disciplined"] if t_size <= position_size else t["oversized"]
        new_row = {"Date": t_date, "Asset": t_asset, "Actual Size": t_size, "Entry Price": t_entry, f'P&L ({currency})': t_pnl, "Status": status}
        st.session_state.journal_data = pd.concat([st.session_state.journal_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success(t["success"])

if not st.session_state.journal_data.empty:
    st.dataframe(st.session_state.journal_data, use_container_width=True)
