import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Institutional Trading & Academy SaaS", layout="wide", page_icon="⚡")

# --- التنقل بين أقسام المنصة ---
st.sidebar.markdown("### 🧭 تنقل بين أقسام المنصة")
app_mode = st.sidebar.selectbox("اختر الصفحة:", ["⚡ محرك التداول الذكي", "🎓 الأكاديمية الذكية والموجه المؤسسي الشامل"])

# ==========================================
# الصفحة الأولى: محرك التداول الذكي
# ==========================================
if app_mode == "⚡ محرك التداول الذكي":

    def calculate_tharp_position_size(capital: float, risk_pct: float, current_price: float, stop_loss_price: float):
        allowed_risk_cash = capital * (risk_pct / 100.0)
        risk_per_share = abs(current_price - stop_loss_price)
        if risk_per_share <= 0:
            return 0, 0.0, 0.0
        shares = int(allowed_risk_cash / risk_per_share)
        total_cost = shares * current_price
        return shares, allowed_risk_cash, total_cost

    def get_murphy_trend_filter(hist_data, current_price: float):
        if hist_data is None or len(hist_data) < 10:
            return "LONG", "بيانات غير كافية لتطبيق مرجع جون ميرفي"
        sma_10 = hist_data['Close'].rolling(window=10).mean().iloc[-1]
        window_30 = min(30, len(hist_data))
        sma_30 = hist_data['Close'].rolling(window=window_30).mean().iloc[-1]
        if current_price >= sma_10 and sma_10 >= sma_30:
            return "LONG", "اتجاه صاعد متوافق مع معايير جون ميرفي (SMA 10/30)"
        elif current_price <= sma_10 and sma_10 <= sma_30:
            return "SHORT", "اتجاه هابط مؤكد (معايير التحليل الفني الكلاسيكي)"
        else:
            direction = "LONG" if current_price >= sma_10 else "SHORT"
            return direction, "منطقة تذبذب عرضي / يتطلب الحذر"

    def get_buffett_fundamental_analysis(info: dict):
        score = 0
        notes = []
        roe = info.get("returnOnEquity")
        pe = info.get("trailingPE")
        profit_margins = info.get("profitMargins")
        
        if roe and roe > 0.12:
            score += 40
            notes.append(f"العائد على حقوق المساهمين ممتاز (ROE: {roe*100:.1f}%)")
        else:
            notes.append("العائد على حقوق المساهمين منخفض أو غير متوفر")
            
        if pe and 0 < pe < 25:
            score += 40
            notes.append(f"مكرر الربحية معقول وجذاب استثمارياً (P/E: {pe:.1f})")
        elif pe and pe >= 25:
            score += 20
            notes.append(f"السهم يتداول بتقييم مرتفع (P/E: {pe:.1f})")
        else:
            notes.append("بيانات مكرر الربحية غير متاحة بدقة")
            
        if profit_margins and profit_margins > 0.10:
            score += 20
            notes.append("هامش ربحية تشغيلي قوي (> 10%)")
        else:
            notes.append("هوامش الربحية تحتاج لمزيد من المتابعة")
            
        if score >= 70:
            rating = "سهم ذو قيمة عالية (Buffett Quality Pick)"
        elif score >= 40:
            rating = "سهم متوسط الجودة الأساسية"
        else:
            rating = "لا يمرر شروط القيمة الاستثمارية الصارمة"
            
        return score, rating, notes

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ إعدادات المحفظة وإدارة المخاطر")
    global_capital = st.sidebar.number_input("رأس المال الكلي (SAR/USD)", value=50000.0, step=1000.0)
    max_risk_pct = st.sidebar.slider("المخاطرة المسموحة للمحفظة (%)", 0.5, 3.0, 1.0)
    market_type = st.sidebar.selectbox("السوق المستهدف", ["السعودي (Tadawul)", "الأمريكي (US)"])
    st.sidebar.success("المحرك يعمل بكامل القواعد الثلاثية (Tharp - Murphy - Buffett)")

    st.markdown("### ⚡ المنصة الاستثمارية المزودة بالقواعد المؤسسية وثلاثية العباقرة")
    st.caption("تدمج بين إدارة المخاطر (فان ثارث)، الزخم والاتجاه (جون ميرفي)، وفلسفة تقييم الشركات (وارن بافيت).")

    col_m1, col_m2, col_m3 = st.columns([1, 1, 2])
    with col_m1:
        raw_ticker = st.text_input("رمز السهم", value="1120" if "السعودي" in market_type else "AAPL")
    with col_m2:
        selected_period = st.selectbox("الفترة الزمنية للتحليل", ["1mo", "3mo", "6mo", "1y"], index=1)
    with col_m3:
        trade_style = st.selectbox("نمط التداول", ["مضاربة سريعة (Day Trading)", "استثمار طويل الأجل (Buffett Style)"])

    if "السعودي" in market_type and not raw_ticker.endswith(".SR"):
        ticker = raw_ticker.strip() + ".SR"
    else:
        ticker = raw_ticker.strip()

    current_price = 0.0
    company_name = "جاري التحليل..."
    auto_direction = "LONG"
    trend_note = "تحليل الزخم"
    info = {}
    hist = None

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=selected_period)
        info = stock.info
        if not hist.empty:
            current_price = float(hist['Close'].iloc[-1])
            auto_direction, trend_note = get_murphy_trend_filter(hist, current_price)
                
        company_name = info.get("longName") or info.get("shortName") or ticker
    except Exception:
        company_name = "خطأ في الرمز أو الاتصال"
        current_price = 0.0

    buffett_score, buffett_rating, buffett_notes = get_buffett_fundamental_analysis(info)

    st.markdown("---")
    st.subheader("📊 ملخص التحليل الفني والمالي للسهم")

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.info(f"**الشركة:** {company_name}\n\n**رمز السهم:** `{ticker}`\n\n**السعر الحالي:** `{current_price:,.2f}`\n\n**الفترة الزمنية:** `{selected_period}`")
    with col_res2:
        direction_color = "🟢 صاعد" if auto_direction == "LONG" else "🔴 هابط"
        st.success(f"**اتجاه الزخم الفني:** {direction_color}\n\n**تفاصيل التحليل:** {trend_note}\n\n**تقييم وارن بافيت:** {buffett_rating} (الدرجة: {buffett_score}/100)")

    with st.expander("تفاصيل تقييم الأساسيات المالية (على طريقة وارن بافيت)"):
        for note in buffett_notes:
            st.write(f"- {note}")

    if "مضاربة" in trade_style:
        sl_percent = 1.5
        target_multiplier = 2.5
        style_label = "مضاربة سريعة"
    else:
        sl_percent = 7.0 
        target_multiplier = 4.0
        style_label = "استثمار بافيتي طويل الأجل"

    if auto_direction == "LONG":
        auto_sl = round(current_price * (1 - (sl_percent / 100)), 2)
        risk_per_share = current_price - auto_sl
        auto_tp = round(current_price + (risk_per_share * target_multiplier), 2)
    else:
        auto_sl = round(current_price * (1 + (sl_percent / 100)), 2)
        risk_per_share = auto_sl - current_price
        auto_tp = round(current_price - (risk_per_share * target_multiplier), 2)

    st.warning(f"🎯 **خطة المحرك الذكي ({style_label}):** الاتجاه (**{auto_direction}**) | وقف الخسارة = **{auto_sl}** | الهدف المقترح = **{auto_tp}** (عائد 1:{target_multiplier})")

    if st.button("🚀 اعتماد وتنفيذ الصفقة بمعايير العباقرة الثلاثة", use_container_width=True):
        shares_count, allowed_risk_cash, total_cost = calculate_tharp_position_size(
            global_capital, max_risk_pct, current_price, auto_sl
        )
        potential_profit = shares_count * abs(auto_tp - current_price)
        
        st.markdown("### لوحة القرار المؤسسي المعتمد")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("الكمية المحسوبة", f"{shares_count:,} سهم")
        m2.metric("إجمالي تكلفة الصفقة", f"{total_cost:,.2f}")
        m3.metric("مخاطر الخسارة القصوى", f"-{allowed_risk_cash:,.2f}", delta_color="inverse")
        m4.metric("الأرباح المستهدفة", f"+{potential_profit:,.2f}", delta="مستهدف")
        
        st.success("تمت العملية بنجاح باستخدام تكامل قواعد المخاطر (فان ثارث)، الاتجاهات الفنية (جون ميرفي)، وتقييم الشركات (وارن بافيت).")


# ==========================================
# الصفحة الثانية: الأكاديمية الذكية والموجه المؤسسي الشامل
# ==========================================
else:
    st.markdown("### 🎓 الأكاديمية الذكية والموجه المؤسسي الشامل")
    st.caption("المرجع الأكاديمي الشامل المدعوم بالذكاء الاصطناعي لفهم التحليل الفني، الكمي، والمالي بعمق مؤسسي.")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 المتوسطات والزخم", 
        "🕯️ الشموع اليابانية", 
        "📐 النماذج الفنية الكلاسيكية", 
        "📊 التحليل الكمي والرياضي", 
        "💰 التحليل المالي الأساسي", 
        "🤖 مساعد الذكاء الاصطناعي الذكي"
    ])

    with tab1:
        st.subheader("المتوسطات المتحركة ومؤشرات الزخم المتقدمة")
        st.markdown("""
        * **المتوسط المتحرك البسيط والآسي (SMA & EMA):** يوضح الاتجاه العام ويصفي الضوضاء السعرية. المتوسطات القصيرة (10 و30) تعكس الزخم اللحظي، بينما المتوسطات الطويلة (100 و200) تحدد الاتجاه الاستثماري المسيطر.
        * **مؤشر القوة النسبية (RSI):** يقيس سرعة التغيرات السعرية لتحديد مناطق تشبع الشراء (أ فوق 70) وتشبع البيع (تحت 30).
        * **مؤشر الـ MACD:** يقيس تقارب وتباعد المتوسطات الأسية لتوليد إشارات دخول وخروج عند تقاطع خط الإشارة مع الهيستوجرام.
        * **بولينجر باند (Bollinger Bands):** يقيس تقلبات السوق؛ تضيق الأشرطة ينذر بانفجار سعري قادم، واتساعها يعكس ذروة الحركة.
        """)

    with tab2:
        st.subheader("دليل الشموع اليابانية وقراءتها النفسية")
        st.markdown("""
        * **المطرقة والشهاب (Hammer & Shooting Star):** شموع ذات ظلال طويلة تدل على رفض الأسعار في القيعان أو القمم وانعكاس الاتجاه المحتمل.
        * **الابتلاع الشرائي والبيعي (Bullish & Bearish Engulfing):** شمعة كاملة تبتلع الشمعة السابقة بالكامل، مؤكدة سيطرة المشترين أو البائعين بقوة.
        * **الجنود الثلاثة البيض والغربان السود (Three White Soldiers / Black Crows):** نماذج استمرارية أو انعكاسية قوية تتألف من ثلاث شموع متتالية باتجاه واحد.
        * **الدوجي والقمم الدوارة (Doji & Spinning Tops):** تعكس حالة تردد وترقب بين قوى العرض والطلب.
        """)

    with tab3:
        st.subheader("النماذج الفنية الكلاسيكية (Chart Patterns)")
        st.markdown("""
        * **الرأس والكتفان (Head & Shoulders):** نموذج انعكاسي كلاسيكي للقمم، حيث يتم قياس الهدف الهابط من نقطة كسر خط العنق بمسافة تساوي ارتفاع الرأس عن الخط.
        * **القاع المزدوج والقمة المزدوجة (Double Bottom / Top):** اختبار متكرر لمستوى دعم أو مقاومة رئيسي يعقبه ارتداد حاد.
        * **المثلثات والمتماثلة والأعلام (Triangles & Flags):** نماذج استمرارية تؤكد أن السعر في استراحة مؤقتة ضمن نفس اتجاه الترند العام.
        * **الكوب والعروة (Cup and Handle):** من أقوى نماذج الاستمرار الصاعد في الأسهم الاستثمارية والنموية.
        """)

    with tab4:
        st.subheader("التحليل الكمي والرياضي في التداول (Quantitative Analysis)")
        st.markdown("""
        * **إدارة المخاطر الرياضية (Van K. Tharp R-Multiples):** قياس العائد الفعلي مقارنة بالمخاطرة الأساسية المحددة مسبقاً (R) لتقييم كفاءة المتداول.
        * **التحليل الإحصائي للتقلبات (Volatility & Variance):** قياس الانحراف المعياري للأسعار التاريخية لتقدير احتمالات المخاطر وتحقيق الأهداف.
        * **العائد مقابل المخاطرة (Risk-to-Reward Ratio):** ضمان ألا تقل نسبة العائد المستهدف عن ضعف أو ثلاثة أضعاف حجم المخاطرة المقبولة.
        """)

    with tab5:
        st.subheader("التحليل المالي الأساسي وقيمة الشركات (Warren Buffett Model)")
        st.markdown("""
        * **العائد على حقوق المساهمين (ROE):** مؤشر رئيسي لمدى كفاءة الإدارة في توليد الأرباح من أموال المستثمرين.
        * **مكرر الربحية وقيمة الأصول (P/E & P/B Ratios):** تقييم ما إذا كان السهم يتداول بسعر رخيص مقارنة بأرباحه وأصوله الحقيقية.
        * **هامش الأمان (Margin of Safety):** مبدأ بافيتي أساسي بعدم شراء أي أصل إلا إذا كان سعره السوقي أقل بكثير من قيمته الجوهرية.
        """)

    with tab6:
        st.subheader("🤖 الموجه الذكي التفاعلي المتعمق")
        st.markdown("اختر استفسارك أو موضوعك المفضل للحصول على شرح وتحليل فوري مدعوم بالذكاء الاصطناعي المؤسسي:")
        
        user_inquiry = st.selectbox(
            "اختر موضوع الشرح والمراجعة:",
            [
                "اشرح لي كيفية دمج مؤشر RSI مع المتوسطات المتحركة بفعالية",
                "ما هي الطريقة العلمية لتحديد وقف الخسارة والهدف وفق فان ثارث؟",
                "كيف تفحص الميزة التنافسية للشركة (Economic Moat) على طريقة وارن بافيت؟",
                "ما هي شروط نجاح النماذج الفنية الكلاسيكية وتجنب الإشارات الوهمية؟"
            ]
        )

        if st.button("✨ توليد الشرح والتحليل الفوري", use_container_width=True):
            if "RSI" in user_inquiry:
                st.success("💡 **تحليل الموجه الذكي (RSI + المتوسطات):**\n\nعندما يكون السهم فوق متوسط 30 ويكون مؤشر RSI صاعداً من مناطق تشبع البيع (تحت 30)، فهذه من أقوى إشارات الدخول الآمن. تجنب البيع أو الشراء لمجرد وصول RSI لرقم 70 في الترندات القوية لأن السهم قد يظل في مناطق تشبع الشراء لفترات طويلة.")
            elif "فان ثارث" in user_inquiry:
                st.success("💡 **تحليل الموجه الذكي (إدارة المخاطر لـ فان ثارث):**\n\nالسر ليس في أين تشتري، بل في أين تخرج إذا كنت مخطئاً. حدد نقطة وقف الخسارة عند كسر هيكل فني معتبر (مثل دعم أو قاع)، وحدد المخاطرة بـ 1% من رأس مالك، واجعل الهدف يغطي أضعاف المخاطرة (R:R بنسبة 1:3 أو أكثر).")
            elif "وارن بافيت" in user_inquiry:
                st.success("💡 **تحليل الموجه الذكي (الميزة التنافسية وقيمة بافيت):**\n\nبافيت يبحث عن الشركات التي تمتلك 'خندقاً اقتصادياً' (Economic Moat) مثل العلامة التجارية القوية، الاحتكار، أو كفاءة التكلفة العالية، والتي تتيح لها تحقيق عائد على حقوق المساهمين (ROE) يفوق 15% باستمرار ودون ديون مفرطة.")
            else:
                st.success("💡 **تحليل الموجه الذكي (النماذج الفنية):**\n\nأهم شروط نجاح أي نموذج فني هو حدوثه بعد اتجاه واضح (ترند سابق)، وضرورة ترافقه مع تزايد ملحوظ في أحجام التداول (Volume) عند لحظة اختراق خط الرقبة أو المقاومة الرئيسية.")