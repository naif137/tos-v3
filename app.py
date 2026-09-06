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
    "subtitle": "Professional Trading Journal, Risk & Multi-Target Engine" if lang == "English" else "سجل التداول الاحترافي، إدارة المخاطر والأهداف المتعددة",
    "account_settings": "📊 Account Settings" if lang == "English" else "📊 إعدادات الحساب",
    "capital": "Starting Capital" if lang == "English" else "رأس المال الأساسي",
    "risk_pct": "Risk Per Trade (%)" if lang == "English" else "نسبة المخاطرة لكل صفقة (%)",
    "risk_terminal": "🎯 1. Pre-Trade Risk Terminal" if lang == "English" else "🎯 1. محطة المخاطر قبل الصفقة",
    "asset": "Asset / Ticker" if lang == "English" else "الرمز / السهم",
    "entry": "Planned Entry" if lang == "English" else "سعر الدخول المستهدف",
    "sl": "Stop Loss" if lang == "English" else "وقف الخسارة",
    "tp1": "Take Profit 1 (TP1)" if lang == "English" else "هدف أول (TP1)",
    "tp2": "Take Profit 2 (TP2)" if lang == "English" else "هدف ثاني (TP2)",
    "risk_analysis": "### Risk & Targets Analysis" if lang == "English" else "### تحليل المخاطر والأهداف",
    "rr1": "R:R (TP1)" if lang == "English" else "العائد للمخاطرة (TP1)",
    "rr2": "R:R (TP2)" if lang == "English" else "العائد للمخاطرة (TP2)",
    "pos_size": "Required Position Size" if lang == "English" else "حجم المركز المطلوب",
    "hard_stop": "🚨 HARD STOP: Poor R:R ratio (< 1.5), Trade Rejected!" if lang == "English" else "🚨 توقف إجباري: نسبة العائد للمخاطرة ضعيفة (< 1.5)، الصفقة مرفوضة!",
    "approved": "🟢 APPROVED: Trade meets risk parameters!" if lang == "English" else "🟢 مسموح: الصفقة تتوافق مع معايير المخاطرة!",
    "journal_title": "📓 2 & 3. Active Trades & Multi-Target Journal" if lang == "English" else "📓 2 & 3. الصفقات النشطة وسجل الأهداف المتعددة",
    "behavior_title": "🧠 4. Behavioral & Psychology Engine" if lang == "English" else "🧠 4. محرك الانضباط والسلوكيات النفسية",
    "date": "Date" if lang == "English" else "التاريخ",
    "actual_size": "Actual Size" if lang == "English" else "الكمية الفعلية",
    "actual_entry": "Actual Entry" if lang == "English" else "سعر الدخول الفعلي",
    "pnl": "Realized P&L" if lang == "English" else "الربح/الخسارة المحققة",
    "record_btn": "Execute & Record Trade" if lang == "English" else "تنفيذ وتسجيل الصفقة",
    "success": "Trade executed and recorded successfully!" if lang == "English" else "تم تنفيذ وتسجيل الصفقة بنجاح!",
    "disciplined": "Disciplined (منضبط)" if lang == "English" else "منضبط (Disciplined)",
    "oversized": "Over-sized (حجم زائد)" if lang == "English" else "كمية زائدة (Over-sized)",
    "fomo": "FOMO / Chasing (ملاحقة السعر)" if lang == "English" else "ملاحقة السعر / FOMO",
    "revenge": "Revenge Trading (انتقام من السوق)" if lang == "English" else "انتقام من السوق (Revenge)",
    "status": "Behavior Status" if lang == "English" else "الحالة السلوكية"
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

# 1. إعدادات الحساب
st.sidebar.header(t["account_settings"])
capital = st.sidebar.number_input(f'{t["capital"]} ({currency})', value=100000.0, step=1000.0)
risk_pct = st.sidebar.slider(t["risk_pct"], min_value=0.1, max_value=5.0, value=0.5) / 100.0

# 2. محطة المخاطر قبل الصفقة (القسم الأول والثالث)
st.subheader(t["risk_terminal"])
col1, col2, col3, col4 = st.columns(4)

with col1:
    asset = st.text_input(t["asset"], value=default_ticker)
    planned_entry = st.number_input(t["entry"], value=180.0)

with col2:
    stop_loss = st.number_input(t["sl"], value=177.5)

with col3:
    tp1 = st.number_input(t["tp1"], value=185.0)
    tp2 = st.number_input(t["tp2"], value=190.0)

with col4:
    st.markdown(t["risk_analysis"])
    risk_amount = capital * risk_pct
    price_diff = abs(planned_entry - stop_loss)
    
    reward_diff1 = abs(tp1 - planned_entry)
    reward_diff2 = abs(tp2 - planned_entry)
    
    rr_ratio1 = reward_diff1 / price_diff if price_diff > 0 else 0
    rr_ratio2 = reward_diff2 / price_diff if price_diff > 0 else 0
    position_size = int(risk_amount / price_diff) if price_diff > 0 else 0
    
    st.metric(label=t["rr1"], value=f"{rr_ratio1:.2f}")
    st.metric(label=t["rr2"], value=f"{rr_ratio2:.2f}")
    st.metric(label=t["pos_size"], value=f"{position_size}")

if rr_ratio1 < 1.5:
    st.error(t["hard_stop"])
else:
    st.success(t["approved"])

st.markdown("---")

# تهيئة جدول الصفقات والسلوكيات (القسم الثاني والرابع)
if "journal_data" not in st.session_state:
    st.session_state.journal_data = pd.DataFrame(columns=[
        "Date", "Asset", "Size", "Entry", "TP1", "TP2", f'P&L ({currency})', "Psychology Status"
    ])

st.subheader(t["journal_title"])

with st.form("trade_form"):
    c1, c2, c3, c4 = st.columns(4)
    t_date = c1.date_input(t["date"], datetime.date.today())
    t_asset = c2.text_input(t["asset"], asset)
    t_size = c3.number_input(t["actual_size"], value=position_size)
    t_entry = c4.number_input(t["actual_entry"], value=planned_entry)
    
    c5, c6, c7, c8 = st.columns(4)
    t_tp1 = c5.number_input(t["tp1"], value=tp1)
    t_tp2 = c6.number_input(t["tp2"], value=tp2)
    t_pnl = c7.number_input(f'{t["pnl"]} ({currency})', value=0.0)
    
    # القسم الرابع: محرك الانضباط النفسي والسلوكي
    st.markdown(t["behavior_title"])
    behavior = st.selectbox("Select State / اختر الحالة النفسية", [t["disciplined"], t["oversized"], t["fomo"], t["revenge"]])
    
    submit_btn = st.form_submit_button(t["record_btn"])
    if submit_btn:
        new_row = {
            "Date": t_date, "Asset": t_asset, "Size": t_size, "Entry": t_entry, 
            "TP1": t_tp1, "TP2": t_tp2, f'P&L ({currency})': t_pnl, "Psychology Status": behavior
        }
        st.session_state.journal_data = pd.concat([st.session_state.journal_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success(t["success"])

if not st.session_state.journal_data.empty:
    st.dataframe(st.session_state.journal_data, use_container_width=True)
