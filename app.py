import streamlit as st
import pandas as pd
import datetime
import yfinance as yf

st.set_page_config(page_title="TOS V3 - Smart Trading Operating System", layout="wide", page_icon="📈")

# --- الإعدادات الجانبية (اللغة والسوق) ---
st.sidebar.header("⚙️ Settings | الإعدادات")
lang = st.sidebar.radio("Language / اللغة", ["عربي", "English"])
market = st.sidebar.selectbox("Market / السوق" if lang == "English" else "السوق", 
                              ["US Market", "Saudi Market"] if lang == "English" else ["السوق الأمريكي", "السوق السعودي"])

is_saudi = "Saudi" in market or "السعودي" in market
currency = "SAR" if is_saudi else "$"
default_ticker = "2222.SR" if is_saudi else "AAPL"

# --- القاموس (عربي/إنجليزي) ---
t = {
    "title": "🚀 TOS V3: AI-Powered Smart Trading System" if lang == "English" else "🚀 نظام TOS V3 الذكي والمطوّر للتداول",
    "subtitle": "Advanced Risk Engine, Smart AI Health Check & Pro Psychology Tracking" if lang == "English" else "محرك المخاطر المتقدم، الفحص الذكي للصحة وتتبع علم النفس الاحترافي",
    "account_settings": "📊 Account Settings" if lang == "English" else "📊 إعدادات الحساب",
    "capital": "Starting Capital" if lang == "English" else "رأس المال الأساسي",
    "risk_pct": "Risk Per Trade (%)" if lang == "English" else "نسبة المخاطرة لكل صفقة (%)",
    "risk_terminal": "🎯 1. AI Smart Risk Terminal" if lang == "English" else "🎯 1. محطة المخاطر والتقييم الذكي للصفقة",
    "asset": "Asset / Ticker" if lang == "English" else "الرمز / السهم",
    "live_price": "Live Market Price" if lang == "English" else "السعر الحي بالسوق",
    "entry": "Planned Entry" if lang == "English" else "سعر الدخول المستهدف",
    "sl": "Stop Loss" if lang == "English" else "وقف الخسارة",
    "tp1": "Take Profit 1 (TP1)" if lang == "English" else "هدف أول (TP1)",
    "tp2": "Take Profit 2 (TP2)" if lang == "English" else "هدف ثاني (TP2)",
    "risk_analysis": "### Risk & AI Health Check" if lang == "English" else "### تحليل المخاطر والفحص الذكي",
    "rr1": "R:R (TP1)" if lang == "English" else "العائد للمخاطرة (TP1)",
    "rr2": "R:R (TP2)" if lang == "English" else "العائد للمخاطرة (TP2)",
    "pos_size": "Required Position Size" if lang == "English" else "حجم المركز المطلوب",
    "hard_stop": "🚨 HARD STOP: Poor R:R ratio (< 1.5), Trade Rejected!" if lang == "English" else "🚨 توقف إجباري: نسبة العائد للمخاطرة ضعيفة (< 1.5)، الصفقة مرفوضة!",
    "approved": "🟢 APPROVED: Trade meets risk parameters!" if lang == "English" else "🟢 مسموح: الصفقة تتوافق مع معايير المخاطرة!",
    "ai_insights": "🤖 AI Trade Intelligence Insights" if lang == "English" else "🤖 رؤى الذكاء الاصطناعي وصحة الصفقة",
    "roadmap_title": "🎓 Pro Trader Roadmap & Mentorship",
    "journal_title": "📓 Smart Active Trades & Psychology Dashboard",
    "backtest_title": "🧪 Backtesting & Training Simulator"
}

# --- تنسيق التصميم واتجاه الشاشة ---
if lang == "عربي":
    st.markdown("""<style>
        .main, .stMarkdown, .stText, [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        .main { background-color: #141619; color: #dcdcdc; }
        h1, h2, h3 { color: #00d296; }
        .stButton>button { background-color: #2d5aid; color: white; border-radius: 5px; width: 100%; }
        .roadmap-box { background-color: #1f242d; padding: 20px; border-radius: 10px; border-left: 5px solid #00d296; margin-bottom: 15px; }
        .ai-box { background-color: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #38bdf8; margin-top: 10px; }
        </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
        .main { background-color: #141619; color: #dcdcdc; }
        h1, h2, h3 { color: #00d296; }
        .stButton>button { background-color: #2d5aid; color: white; border-radius: 5px; width: 100%; }
        .roadmap-box { background-color: #1f242d; padding: 20px; border-radius: 10px; border-left: 5px solid #00d296; margin-bottom: 15px; }
        .ai-box { background-color: #1e293b; padding: 15px; border-radius: 8px; border: 1px solid #38bdf8; margin-top: 10px; }
        </style>""", unsafe_allow_html=True)

# --- واجهة التطبيق الرئيسية ---
st.title(t["title"])
st.markdown(t["subtitle"])

# الإعدادات الجانبية للحساب
st.sidebar.header(t["account_settings"])
capital = st.sidebar.number_input(f'{t["capital"]} ({currency})', value=100000.0, step=1000.0)
risk_pct = st.sidebar.slider(t["risk_pct"], min_value=0.1, max_value=5.0, value=0.5) / 100.0

# --- مسار الاحتراف (مختصر ونظيف) ---
with st.expander("🎓 عرض مسار المحترف وقواعد التداول السليمة (Pro Roadmap)", expanded=False):
    st.markdown("""
    * **المرحلة 1:** حماية رأس المال بعدم المخاطرة بأكثر من 0.5%-1% لكل صفقة.
    * **المرحلة 2:** الالتزام بالدخول بناءً على اتجاه السوق والهيكل الفني.
    * **المرحلة 3:** ترويض النفسية وتجنب ملاحقة الأسعار (FOMO) والانتقام.
    * **المرحلة 4:** تفعيل الباك تست وإثبات ربحية الاستراتيجية إحصائياً.
    """)

st.markdown("---")

# 1. محطة المخاطر الذكية
st.subheader(t["risk_terminal"])
col1, col2, col3, col4 = st.columns(4)

with col1:
    user_input_asset = st.text_input(t["asset"], value="1120" if is_saudi else "AAPL")
    query_asset = user_input_asset.strip()
    if is_saudi and not query_asset.endswith(".SR") and not query_asset.endswith(".sr"):
        query_asset = query_asset + ".SR"

    current_market_price = 180.0
    comp_name = "N/A"
    try:
        ticker_obj = yf.Ticker(query_asset)
        info = ticker_obj.info
        comp_name = info.get('longName', info.get('shortName', query_asset))
        
        todays_data = ticker_obj.history(period="1d")
        if not todays_data.empty:
            current_market_price = float(todays_data['Close'].iloc[-1])
            st.success(f"🏢 {comp_name}\n\n💰 {t['live_price']}: {current_market_price:.2f} {currency}")
        else:
            st.warning("⚠️ تعذر جلب السعر اللحظي")
    except Exception:
        st.warning("⚠️ استخدام القيمة الافتراضية")

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

# --- نظام التقييم والفحص الذكي (AI Health Check) ---
st.markdown(f"### {t['ai_insights']}")
ai_tips = []
if price_diff > 0:
    sl_distance_pct = (abs(planned_entry - stop_loss) / planned_entry) * 100
    if sl_distance_pct < 1.0:
        ai_tips.append("⚠️ **تحذير وقف الخسارة:** المسافة لوقف الخسارة ضيقة جداً (<1%) وقد يتم ضربه بالتذبذب الطبيعي للسوق.")
    if sl_distance_pct > 7.0:
        ai_tips.append("⚠️ **مسافة الوقف واسعة:** وقف الخسارة بعيد نسبياً، تأكد أن حجم المركز يتناسب مع هذه المخاطرة.")
    if rr_ratio1 >= 2.5:
        ai_tips.append("🌟 **أداء ممتاز:** نسبة العائد للمخاطرة للهدف الأول قوية جداً وتفوق 2.5.")
    if not ai_tips:
        ai_tips.append("✅ **الحالة العامة سليمة:** معايير الدخول والوقف تتوافق مع القواعد القياسية المعتمدة.")

for tip in ai_tips:
    st.markdown(f"<div class='ai-box'>{tip}</div>", unsafe_allow_html=True)

st.markdown("---")

# 2 & 3. سجل الصفقات الذكي وتتبع مؤشر الأداء النفسي
if "journal_data" not in st.session_state:
    st.session_state.journal_data = pd.DataFrame(columns=[
        "Date", "Asset", "Size", "Entry", "TP1", "TP2", f'P&L ({currency})', "Psychology Status"
    ])

st.subheader(t["journal_title"])

with st.form("trade_form"):
    c1, c2, c3, c4 = st.columns(4)
    t_date = c1.date_input("Date", datetime.date.today())
    t_asset = c2.text_input("Asset", user_input_asset)
    t_size = c3.number_input("Size", value=position_size)
    t_entry = c4.number_input("Entry", value=planned_entry)
    
    c5, c6, c7, c8 = st.columns(4)
    t_tp1 = c5.number_input("TP1", value=tp1)
    t_tp2 = c6.number_input("TP2", value=tp2)
    t_pnl = c7.number_input(f'P&L ({currency})', value=0.0)
    
    behavior = c8.selectbox("Psychology State", ["Disciplined (منضبط)", "Over-sized (حجم زائد)", "FOMO (ملاحقة السعر)", "Revenge (انتقام)"])
    
    submit_btn = st.form_submit_button("Execute & Record Trade")
    if submit_btn:
        new_row = {
            "Date": t_date, "Asset": t_asset, "Size": t_size, "Entry": t_entry, 
            "TP1": t_tp1, "TP2": t_tp2, f'P&L ({currency})': t_pnl, "Psychology Status": behavior
        }
        st.session_state.journal_data = pd.concat([st.session_state.journal_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Trade recorded successfully!")

if not st.session_state.journal_data.empty:
    st.dataframe(st.session_state.journal_data, use_container_width=True)
    
    # مؤشر الأداء النفسي والالتزام الذكي
    total_trades_count = len(st.session_state.journal_data)
    disciplined_count = len(st.session_state.journal_data[st.session_state.journal_data['Psychology Status'].str.contains("Disciplined|منضبط")])
    discipline_score = (disciplined_count / total_trades_count) * 100 if total_trades_count > 0 else 0
    
    st.markdown(f"### 🧠 مؤشر الالتزام الانضباطي النفسي: `{discipline_score:.1f}%`")
    st.progress(discipline_score / 100.0)
