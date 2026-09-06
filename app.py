import streamlit as st
import pandas as pd
import datetime
import yfinance as yf

st.set_page_config(page_title="TOS V3 - Institutional Grade AI Trading System", layout="wide", page_icon="📈")

# --- الإعدادات الجانبية (اللغة والسوق) ---
st.sidebar.header("⚙️ Settings | إعدادات النظام المؤسسي")
lang = st.sidebar.radio("Language / اللغة", ["عربي", "English"])
market = st.sidebar.selectbox("Market / السوق" if lang == "English" else "السوق", 
                              ["US Market", "Saudi Market"] if lang == "English" else ["السوق الأمريكي", "السوق السعودي"])

is_saudi = "Saudi" in market or "السعودي" in market
currency = "SAR" if is_saudi else "$"
default_ticker = "2222.SR" if is_saudi else "AAPL"

# --- القاموس (عربي/إنجليزي) ---
t = {
    "title": "🚀 TOS V3: Institutional AI Trading & Risk Engine" if lang == "English" else "🚀 نظام TOS V3: الذكاء الاصطناعي المؤسسي لإدارة التداول والمخاطر",
    "subtitle": "Advanced Quantitative Edge, Automated Psychology Audit & Dynamic Capital Management" if lang == "English" else "أفضلية كمية متقدمة، تدقيق نفسي آلي، وإدارة ديناميكية لرأس المال",
    "account_settings": "📊 Institutional Account Settings" if lang == "English" else "📊 إعدادات المحفظة المؤسسية",
    "capital": "Starting Capital" if lang == "English" else "رأس المال الأساسي",
    "risk_pct": "Risk Per Trade (%)" if lang == "English" else "نسبة المخاطرة لكل صفقة (%)",
    "risk_terminal": "🎯 1. Quantitative Pre-Trade Risk Terminal" if lang == "English" else "🎯 1. محطة المخاطر والتحليل الكمي المسبق",
    "asset": "Asset / Ticker" if lang == "English" else "الرمز / السهم",
    "live_price": "Live Market Price" if lang == "English" else "السعر الحي بالسوق",
    "entry": "Planned Entry" if lang == "English" else "سعر الدخول المستهدف",
    "sl": "Stop Loss" if lang == "English" else "وقف الخسارة",
    "tp1": "Take Profit 1 (TP1)" if lang == "English" else "هدف أول (TP1)",
    "tp2": "Take Profit 2 (TP2)" if lang == "English" else "هدف ثاني (TP2)",
    "risk_analysis": "### Quantitative Risk Metrics" if lang == "English" else "### مقاييس المخاطر الكمية",
    "rr1": "R:R (TP1)" if lang == "English" else "العائد للمخاطرة (TP1)",
    "rr2": "R:R (TP2)" if lang == "English" else "العائد للمخاطرة (TP2)",
    "pos_size": "Optimal Position Size" if lang == "English" else "حجم المركز الأمثل",
    "hard_stop": "🚨 HARD STOP: Poor R:R ratio (< 1.5), Trade Rejected by Risk Engine!" if lang == "English" else "🚨 توقف إجباري: نسبة العائد للمخاطرة ضعيفة (< 1.5)، محطة المخاطر ترفض الصفقة!",
    "approved": "🟢 APPROVED: Trade meets institutional parameters!" if lang == "English" else "🟢 معتمد: الصفقة تتوافق مع معايير المؤسسة!",
    "ai_insights": "🤖 Institutional AI Health & Psychology Diagnostic" if lang == "English" else "🤖 التشخيص الذكي المؤسسي للصحة النفسية وإدارة المخاطر",
    "journal_title": "📓 Advanced Trade Journal & Performance Analytics" if lang == "English" else "📓 سجل الصفقات المتقدم وتحليلات الأداء الشاملة"
}

# --- تنسيق التصميم المؤسسي ---
if lang == "عربي":
    st.markdown("""<style>
        .main, .stMarkdown, .stText, [data-testid="stSidebar"] { direction: rtl; text-align: right; }
        .main { background-color: #0e1117; color: #e2e8f0; }
        h1, h2, h3 { color: #10b981; }
        .stButton>button { background-color: #059669; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
        .ai-audit-box { background-color: #182232; padding: 18px; border-radius: 10px; border-left: 5px solid #38bdf8; margin-top: 10px; margin-bottom: 10px; }
        .warning-box { background-color: #2b1d1d; padding: 18px; border-radius: 10px; border-left: 5px solid #ef4444; margin-top: 10px; margin-bottom: 10px; }
        </style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>
        .main { background-color: #0e1117; color: #e2e8f0; }
        h1, h2, h3 { color: #10b981; }
        .stButton>button { background-color: #059669; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
        .ai-audit-box { background-color: #182232; padding: 18px; border-radius: 10px; border-left: 5px solid #38bdf8; margin-top: 10px; margin-bottom: 10px; }
        .warning-box { background-color: #2b1d1d; padding: 18px; border-radius: 10px; border-left: 5px solid #ef4444; margin-top: 10px; margin-bottom: 10px; }
        </style>""", unsafe_allow_html=True)

# --- واجهة التطبيق الرئيسية ---
st.title(t["title"])
st.markdown(t["subtitle"])

# إعدادات الحساب المؤسسي
st.sidebar.header(t["account_settings"])
capital = st.sidebar.number_input(f'{t["capital"]} ({currency})', value=100000.0, step=1000.0)
risk_pct = st.sidebar.slider(t["risk_pct"], min_value=0.1, max_value=3.0, value=0.5) / 100.0

st.markdown("---")

# 1. محطة المخاطر والتحليل الكمي المسبق
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
            st.warning("⚠️ تعذر جلب السعر الحي")
    except Exception:
        st.warning("⚠️ استخدام السعر الافتراضي")

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

# --- محرك الذكاء الاصطناعي للتدقيق الفوري للصحة والصفقة ---
st.markdown(f"### {t['ai_insights']}")
ai_audit_messages = []
if price_diff > 0:
    sl_pct = (abs(planned_entry - stop_loss) / planned_entry) * 100
    if sl_pct < 0.8:
        ai_audit_messages.append(("warning", "⚠️ **تحذير هيكلي:** وقف الخسارة قريب للغاية (<0.8%)، مما يجعله عرضة للضرب العشوائي بفعل صانع السوق."))
    elif sl_pct > 6.0:
        ai_audit_messages.append(("warning", "⚠️ **تنبيه مخاطر:** مسافة وقف الخسارة واسعة (>6%)، تأكد من تقليل حجم العقد لئلا تتجاوز الخسارة المستهدفة."))
    
    if rr_ratio1 >= 3.0:
        ai_audit_messages.append(("info", "🌟 **أفضلية عالية:** صفقة ذات هيكل ممتاز وعائد للمخاطرة يتجاوز 3:1، ينصح بتنفيذها بحذر وانضباط."))
    elif not ai_audit_messages:
        ai_audit_messages.append(("info", "✅ **تقييم متوازن:** معايير الدخول والوقف والخروج ضمن الحدود الآمنة للاستراتيجية."))

for m_type, msg in ai_audit_messages:
    if m_type == "warning":
        st.markdown(f"<div class='warning-box'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-audit-box'>{msg}</div>", unsafe_allow_html=True)

st.markdown("---")

# 2 & 3. سجل الصفقات المؤسسي المتقدم وتحليلات الأداء الشاملة
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
    
    submit_btn = st.form_submit_button("Execute & Record Trade in Journal")
    if submit_btn:
        new_row = {
            "Date": t_date, "Asset": t_asset, "Size": t_size, "Entry": t_entry, 
            "TP1": t_tp1, "TP2": t_tp2, f'P&L ({currency})': t_pnl, "Psychology Status": behavior
        }
        st.session_state.journal_data = pd.concat([st.session_state.journal_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("Trade securely recorded in institutional journal!")

if not st.session_state.journal_data.empty:
    st.dataframe(st.session_state.journal_data, use_container_width=True)
    
    # --- لوحة المؤشرات الكمية والأداء النفسي المتقدم ---
    st.markdown("### 📊 لوحة التحليلات الكمية والأداء النفسي المتقدم")
    
    total_trades = len(st.session_state.journal_data)
    total_pnl = st.session_state.journal_data[f'P&L ({currency})'].sum()
    winning_trades = len(st.session_state.journal_data[st.session_state.journal_data[f'P&L ({currency})'] > 0])
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    disciplined_count = len(st.session_state.journal_data[st.session_state.journal_data['Psychology Status'].str.contains("Disciplined|منضبط")])
    discipline_score = (disciplined_count / total_trades) * 100 if total_trades > 0 else 0
    
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    q_col1.metric("إجمالي الصفقات", f"{total_trades}")
    q_col2.metric("صافي الأرباح/الخسائر", f"{total_pnl:+,.2f} {currency}")
    q_col3.metric("معدل الربحية (Win Rate)", f"{win_rate:.1f}%")
    q_col4.metric("مؤشر الانضباط النفسي", f"{discipline_score:.1f}%")
    
    # تحذير ذكي بناءً على الأداء النفسي
    if discipline_score < 60 and total_trades >= 3:
        st.error("🚨 **تنبيه نفسي خطير:** مؤشر انضباطك منخفض (<60%). النظام يوصي بإيقاف التداول الجلسة الحالية وإعادة مراجعة الخطة لتجنب استنزاف رأس المال.")
    elif discipline_score >= 80:
        st.success("🌟 **أداء احترافي ممتاز:** استمر على هذا الانضباط العالي، التزامك النفسي هو مفتاح استدامة المحفظة على المدى الطويل.")
