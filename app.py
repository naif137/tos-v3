import streamlit as st
import pandas as pd
import datetime
import yfinance as yf

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
    "subtitle": "Professional Trading Journal, Risk & Live Market Data Engine" if lang == "English" else "سجل التداول، إدارة المخاطر وسحب بيانات الأسواق الحية",
    "account_settings": "📊 Account Settings" if lang == "English" else "📊 إعدادات الحساب",
    "capital": "Starting Capital" if lang == "English" else "رأس المال الأساسي",
    "risk_pct": "Risk Per Trade (%)" if lang == "English" else "نسبة المخاطرة لكل صفقة (%)",
    "risk_terminal": "🎯 1. Live Market Risk Terminal" if lang == "English" else "🎯 1. محطة المخاطر والبيانات الحية للسوق",
    "asset": "Asset / Ticker" if lang == "English" else "الرمز / السهم",
    "live_price": "Live Market Price" if lang == "English" else "السعر الحي بالسوق",
    "company_name": "Company" if lang == "English" else "الشركة",
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
    "backtest_title": "🧪 5. Backtesting & Training Simulator" if lang == "English" else "🧪 5. محاكي التدريب والاختبار العكسي (Backtest)",
    "date": "Date" if lang == "English" else "التاريخ",
    "actual_size": "Actual Size" if lang == "English" else "الكمية الفعلية",
    "actual_entry": "Actual Entry" if lang == "English" else "سعر الدخول الفعلي",
    "pnl": "Realized P&L" if lang == "English" else "الربح/الخسارة المحققة",
    "record_btn": "Execute & Record Trade" if lang == "English" else "تنفيذ وتسجيل الصفقة",
    "success": "Trade executed and recorded successfully!" if lang == "English" else "تم تنفيذ وتسجيل الصفقة بنجاح!",
    "disciplined": "Disciplined (منضبط)" if lang == "English" else "منضبط (Disciplined)",
    "oversized": "Over-sized (حجم زائد)" if lang == "English" else "كمية زائدة (Over-sized)",
    "fomo": "FOMO / Chasing (ملاحقة السعر)" if lang == "English" else "ملاحقة السعر / FOMO",
    "revenge": "Revenge Trading (انتقام من السوق)" if lang == "English" else "انتقام من السوق (Revenge)"
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

# الإعدادات الجانبية للحساب
st.sidebar.header(t["account_settings"])
capital = st.sidebar.number_input(f'{t["capital"]} ({currency})', value=100000.0, step=1000.0)
risk_pct = st.sidebar.slider(t["risk_pct"], min_value=0.1, max_value=5.0, value=0.5) / 100.0

# 1. محطة المخاطر وجلب اسم الشركة والسعر الحي
st.subheader(t["risk_terminal"])
col1, col2, col3, col4 = st.columns(4)

with col1:
    asset = st.text_input(t["asset"], value=default_ticker)
    
    current_market_price = 180.0
    comp_name = "N/A"
    try:
        ticker_obj = yf.Ticker(asset)
        # محاولة جلب اسم الشركة
        info = ticker_obj.info
        comp_name = info.get('longName', info.get('shortName', asset))
        
        todays_data = ticker_obj.history(period="1d")
        if not todays_data.empty:
            current_market_price = float(todays_data['Close'].iloc[-1])
            st.success(f"🏢 {comp_name}\n\n💰 {t['live_price']}: {current_market_price:.2f} {currency}")
        else:
            st.warning("⚠️ تعذر جلب السعر اللحظي، يرجى التحقق من الرمز")
    except Exception:
        st.warning("⚠️ جاري استخدام القيمة الافتراضية")

    planned_entry = st.number_input(t["entry"], value=current_market_price)

with col2:
    stop_loss = st.number_input(t["sl"], value=round(current_market_price * 0.98, 2))

with col3:
    tp1 = st.number_input(t["tp1"], value=round(current_market_price * 1.03, 2))
    tp2 = st.number_input(t["tp2"], value=round(current_market_price * 1.06, 2))

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

# 2 & 3 & 4. الصفقات النشطة وسجل الأهداف والسلوكيات
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

st.markdown("---")

# 5. قسم التدريب والباك تست
st.subheader(t["backtest_title"])
st.markdown("اختبر استراتيجيتك التاريخية عبر محاكاة عدد من الصفقات الوهمية لمعرفة نسبة النجاح (Win Rate) المتوقعة.")

bt_col1, bt_col2, bt_col3 = st.columns(3)
with bt_col1:
    bt_trades = st.number_input("عدد الصفقات التجريبية (Total Trades)", value=20, min_value=1)
with bt_col2:
    bt_winrate = st.slider("نسبة نجاح الاستراتيجية المتوقعة (%)", min_value=10.0, max_value=90.0, value=50.0) / 100.0
with bt_col3:
    bt_avg_rr = st.number_input("متوسط العائد للمخاطرة (Average R:R)", value=2.0, min_value=0.5)

if st.button("تشغيل محاكاة الباك تست | Run Backtest Simulation"):
    wins = int(bt_trades * bt_winrate)
    losses = bt_trades - wins
    total_return_units = (wins * bt_avg_rr) - losses
    
    st.success(f"نتائج محاكاة الباك تست لـ {bt_trades} صفقة:")
    res_c1, res_c2, res_c3 = st.columns(3)
    res_c1.metric("الصفقات الرابحة / الخاسرة", f"{wins} Win / {losses} Loss")
    res_c2.metric("محصلة العائد بالوحدات (R)", f"{total_return_units:+.2f} R")
    expectancy = (bt_winrate * bt_avg_rr) - (1 - bt_winrate)
    res_c3.metric("معامل التوقع الإحصائي (Expectancy)", f"{expectancy:+.2f} R per trade")
