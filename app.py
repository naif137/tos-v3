import streamlit as st
import pandas as pd
import datetime
import yfinance as yf

st.set_page_config(page_title="TOS V3 - Ultimate Institutional & Algorithmic System", layout="wide", page_icon="📈")

# --- الإعدادات الجانبية (اللغة والسوق) ---
st.sidebar.header("⚙️ Settings | لوحة التحكم المؤسسية")
lang = st.sidebar.radio("Language / اللغة", ["عربي", "English"])
market = st.sidebar.selectbox("Market / السوق" if lang == "English" else "السوق", 
                              ["US Market", "Saudi Market"] if lang == "English" else ["السوق الأمريكي", "السوق السعودي"])

is_saudi = "Saudi" in market or "السعودي" in market
currency = "SAR" if is_saudi else "$"
default_ticker = "2222.SR" if is_saudi else "AAPL"

# --- القاموس المؤسسي المتكامل ---
t = {
    "title": "🚀 TOS V3: Ultimate Algorithmic Trading & Capital Protection Engine" if lang == "English" else "🚀 نظام TOS V3: المحطة الخارقة للخوارزميات وحماية رأس المال القصوى",
    "subtitle": "Institutional Grade Risk Management, ATR Volatility Stops, Circuit Breakers & Pro Mastery Tracks" if lang == "English" else "إدارة مخاطر مؤسسية، وقفات تذبذب ATR، قواطع أمان للحماية، ومسارات احترافية",
    "account_settings": "📊 Portfolio Parameters" if lang == "English" else "📊 إعدادات المحفظة ورأس المال",
    "capital": "Starting Capital" if lang == "English" else "رأس المال الأساسي",
    "risk_pct": "Max Risk Per Trade (%)" if lang == "English" else "أقصى نسبة مخاطرة لكل صفقة (%)",
    "max_daily_loss": "Max Daily Drawdown Limit (%)" if lang == "English" else "حد الخسارة اليومية القصوى (Circuit Breaker %)",
    "terminal_title": "🎯 1. Algorithmic Pre-Trade Risk & ATR Terminal" if lang == "English" else "🎯 1. محطة المخاطر الخوارزمية وحسابات التذبذب (ATR)",
    "asset": "Asset / Ticker" if lang == "English" else "الرمز / السهم",
    "live_price": "Live Market Price" if lang == "English" else "السعر الحي بالسوق",
    "entry": "Planned Entry" if lang == "English" else "سعر الدخول المستهدف",
    "sl": "Dynamic Stop Loss (ATR Based)" if lang == "English" else "وقف الخسارة الذكي (المبني على التذبذب)",
    "tp1": "Take Profit 1 (TP1)" if lang == "English" else "هدف أول (TP1)",
    "tp2": "Take Profit 2 (TP2)" if lang == "English" else "هدف ثاني (TP2)",
    "metrics_header": "### Quantitative & Volatility Metrics" if lang == "English" else "### المقاييس الكمية ومؤشرات التذبذب",
    "rr1": "R:R (TP1)" if lang == "English" else "العائد للمخاطرة (TP1)",
    "rr2": "R:R (TP2)" if lang == "English" else "العائد للمخاطرة (TP2)",
    "pos_size": "Optimal Position Size" if lang == "English" else "حجم المركز الآمن (أسهم)",
    "hard_stop": "🚨 CIRCUIT BREAKER / HARD STOP: Trade Rejected by Institutional Rules!" if lang == "English" else "🚨 قاطع الأمان مفعل / وقف إجباري: الصفقة مرفوضة وفقاً لقواعد المؤسسة!",
    "approved": "🟢 APPROVED: Trade fully compliant with risk parameters!" if lang == "English" else "🟢 معتمد: الصفقة متوافقة تماماً مع معايير الأمان المالي!",
    "academy_title": "🎓 Pro Mastery Academy & Technical Patterns Track" if lang == "English" else "🎓 أكاديمية المحترف ومسار النماذج الفنية وهيكل السوق",
    "journal_title": "📓 Algorithmic Trade Journal & Psychological Audit" if lang == "English" else "📓 سجل الصفقات الخوارزمي والتدقيق النفسي واليومي"
}

# --- التصميم المؤسسي الفاخر ---
if lang == "عربي":
    st.markdown("""<style>
        .main, .stMarkdown, .stText, [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        .main { background-color: #0b0f19; color: #f1f5f9; }
        h1, h2, h3 { color: #34d399; }
        .stButton>button { background-color: #059669; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
        .inst-box { background-color: #111827; padding: 20px; border-radius: 12px; border-right: 6px solid #34d399; margin-bottom: 15px; }
        .alert-box { background-color: #7f1d1d; padding: 18px; border-radius: 10px; border-right: 6px solid #f87171; margin-top: 10px; }
        .success-box { background-color: #064e3b; padding: 18px; border-radius: 10px; border-right: 6px solid #34d399; margin-top: 10px; }
        </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
        .main { background-color: #0b0f19; color: #f1f5f9; }
        h1, h2, h3 { color: #34d399; }
        .stButton>button { background-color: #059669; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
        .inst-box { background-color: #111827; padding: 20px; border-radius: 12px; border-left: 6px solid #34d399; margin-bottom: 15px; }
        .alert-box { background-color: #7f1d1d; padding: 18px; border-radius: 10px; border-left: 6px solid #f87171; margin-top: 10px; }
        .success-box { background-color: #064e3b; padding: 18px; border-radius: 10px; border-left: 6px solid #34d399; margin-top: 10px; }
        </style>""", unsafe_allow_html=True)

# واجهة التطبيق
st.title(t["title"])
st.markdown(t["subtitle"])

# إعدادات الحساب الجانبية
st.sidebar.header(t["account_settings"])
capital = st.sidebar.number_input(f'{t["capital"]} ({currency})', value=100000.0, step=1000.0)
risk_pct = st.sidebar.slider(t["risk_pct"], min_value=0.1, max_value=2.0, value=0.5) / 100.0
max_daily_drawdown = st.sidebar.slider(t["max_daily_loss"], min_value=1.0, max_value=5.0, value=2.0)

st.markdown("---")

# --- الأداة التفاعلية الكبرى: أكاديمية المحترف والمسار الفني (Pro Mastery & Technical Track) ---
with st.expander(f"📚 {t['academy_title']} (اضغط هنا لفتح مسار التعليم الفني الكامل)", expanded=False):
    st.markdown("""
    <div class="inst-box">
        <h3>المسار التوجيهي الشامل للمتداول المحترف (من الهواية إلى الاحتراف المؤسسي)</h3>
        <p>لكي تضمن أنك لا تخسر، يجب أن تتقن 4 ركائز فنية لا غنى عنها:</p>
        <ul>
            <li><b>1. هيكل السوق وقانون السيولة (Market Structure):</b> لا تشتري لمجرد أن السهم نزل؛ ابحث عن كسر القمة السابقة وتغيير مسار السلم (CHoCH / BOS).</li>
            <li><b>2. مناطق العرض والطلب المؤسسية (Order Blocks):</b> الشراء يكون حصرياً من الشموع التي سبقت الانفجار السعري الصاعد، والبيع عند مناطق الهبوط العنيف.</li>
            <li><b>3. إدارة الحجم الجزئي (Scaling-In Strategy):</b> لا تدخل بكل الكمية دفعة واحدة. أدخل بـ 50% عند الدعم الأول، و50% عند التأكيد، لتقليل تكلفة الدخول.</li>
            <li><b>4. الانضباط الرياضي (Mathematical Expectancy):</b> تداولك عبارة عن نظام احتمالي؛ التزم بنسبة عائد للمخاطرة تتجاوز 2:1 دائماً ودع الإحصاء يعمل لصالحك.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- محطة المخاطر وحسابات التذبذب ATR ---
st.subheader(t["terminal_title"])
col1, col2, col3, col4 = st.columns(4)

with col1:
    user_input_asset = st.text_input(t["asset"], value="1120" if is_saudi else "AAPL")
    query_asset = user_input_asset.strip()
    if is_saudi and not query_asset.endswith(".SR") and not query_asset.endswith(".sr"):
        query_asset = query_asset + ".SR"

    current_market_price = 180.0
    comp_name = "N/A"
    historical_data = None
    try:
        ticker_obj = yf.Ticker(query_asset)
        info = ticker_obj.info
        comp_name = info.get('longName', info.get('shortName', query_asset))
        
        historical_data = ticker_obj.history(period="14d")
        if not historical_data.empty:
            current_market_price = float(historical_data['Close'].iloc[-1])
            st.success(f"🏢 {comp_name}\n\n💰 {t['live_price']}: {current_market_price:.2f} {currency}")
        else:
            st.warning("⚠️ تعذر جلب السعر الحي")
    except Exception:
        st.warning("⚠️ استخدام السعر الافتراضي")

    planned_entry = st.number_input(t["entry"], value=current_market_price)

with col2:
    # حساب تقريبي لـ ATR (مدى التذبذب لآخر 14 يوم لحماية الوقف)
    default_atr = current_market_price * 0.02
    if historical_data is not None and len(historical_data) >= 14:
        high_low = historical_data['High'] - historical_data['Low']
        default_atr = float(high_low.mean())

    suggested_sl = round(planned_entry - (default_atr * 1.5), 2)
    stop_loss = st.number_input(t["sl"], value=max(suggested_sl, 0.01))

with col3:
    tp1 = st.number_input(t["tp1"], value=round(planned_entry + (abs(planned_entry - stop_loss) * 2.0), 2))
    tp2 = st.number_input(t["tp2"], value=round(planned_entry + (abs(planned_entry - stop_loss) * 3.5), 2))

with col4:
    st.markdown(t["metrics_header"])
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

if rr_ratio1 < 1.8:
    st.markdown(f"<div class='alert-box'>{t['hard_stop']} (العائد أقل من 1.8)</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='success-box'>{t['approved']}</div>", unsafe_allow_html=True)

st.markdown("---")

# --- سجل الصفقات والتدقيق النفسي المؤسسي ---
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
    
    behavior = c8.selectbox("Psychology State", ["Disciplined & Patient (منضبط وصبور)", "Over-sized (حجم زائد خاطئ)", "FOMO Chasing (ملاحقة السعر بطمع)", "Revenge Trade (محاولة انتقام خاسرة)"])
    
    submit_btn = st.form_submit_button("Execute & Securely Log Trade")
    if submit_btn:
        new_row = {
            "Date": t_date, "Asset": t_asset, "Size": t_size, "Entry": t_entry, 
            "TP1": t_tp1, "TP2": t_tp2, f'P&L ({currency})': t_pnl, "Psychology Status": behavior
        }
        st.session_state.journal_data = pd.concat([st.session_state.journal_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Trade recorded with algorithmic protection!")

if not st.session_state.journal_data.empty:
    st.dataframe(st.session_state.journal_data, use_container_width=True)
    
    # لوحة التحليل الإحصائي وقاطع الأمان اليومي (Circuit Breaker)
    total_trades = len(st.session_state.journal_data)
    total_pnl = st.session_state.journal_data[f'P&L ({currency})'].sum()
    winning_trades = len(st.session_state.journal_data[st.session_state.journal_data[f'P&L ({currency})'] > 0])
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    # فحص قاطع الأمان (إذا بلغت الخسارة اليومية الحد الأقصى)
    max_allowed_loss_amount = capital * (max_daily_drawdown / 100.0)
    
    st.markdown("### 📊 لوحة الأداء المالي وقاطع الأمان المؤسسي (Circuit Breaker)")
    m_c1, m_c2, m_c3, m_c4 = st.columns(4)
    m_c1.metric("إجمالي الصفقات", f"{total_trades}")
    m_c2.metric("صافي الأرباح المحققة", f"{total_pnl:+,.2f} {currency}")
    m_c3.metric("معدل النجاح الإحصائي", f"{win_rate:.1f}%")
    m_c4.metric("حد الأمان المسموح (Max Loss)", f"-{max_allowed_loss_amount:,.2f} {currency}")
    
    if total_pnl <= -max_allowed_loss_amount:
        st.markdown("""
        <div class="alert-box">
            <h2>🚨 تم تفعيل قاطع الأمان اليومي (CIRCUIT BREAKER ACTIVATED) 🚨</h2>
            <p>لقد تجاوزت خسائرك الحد الأقصى المسموح به لجلسة اليوم. نظماً وقانونياً للمؤسسات، تم إيقاف الصفقات الجديدة إجبارياً لحماية بقية رأس مالك. اغلق الشاشة وعد غداً بيوم جديد برأس مال محمي!</p>
        </div>
        """, unsafe_allow_html=True)
elif not st.session_state.journal_data.empty == False:
    st.info("💡 سجّل صفقاتك أعلاه لتفعيل مؤشرات الأداء وقاطع الأمان اليومي الحصري.")
