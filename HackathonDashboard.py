#streamlit run HackathonDashboard.py

import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import qrcode
from sklearn.ensemble import IsolationForest, RandomForestRegressor
import streamlit as st

# --- PAGE CONFIGURATION (SIDEBAR COLLAPSED BY DEFAULT) ---
st.set_page_config(
    page_title="EcoSmart Campus | Hackathon | Liwa University",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- THEME CSS (CLEAN OFF-WHITE BODY & STYLING) ---
st.markdown(
    """
    <style>
    /* Main Off-White Background */
    .stApp, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #F7F9F6 !important;
        color: #1B3B2B !important;
    }
    
    /* Razor-Sharp Image Rendering for Logos & Graphics */
    img {
        image-rendering: -webkit-optimize-contrast !important;
        image-rendering: crisp-edges !important;
    }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #143625 !important;
        color: #F7F9F6 !important;
    }
    [data-testid="stSidebar"] * {
        color: #F7F9F6 !important;
    }

    /* Typography */
    h1, h2, h3, h4 {
        color: #143625 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    p, li, span, label {
        color: #1E3A2F !important;
    }

    /* PERMANENT BLACK INPUT BOXES & DROPDOWNS WITH WHITE TEXT */
    input, textarea, [data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1px solid #000000 !important;
        border-radius: 6px !important;
    }
    [data-baseweb="select"] span, [data-baseweb="select"] div, [data-baseweb="select"] svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        background-color: #000000 !important;
    }
    ul[role="listbox"], ul[role="listbox"] li {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #1E5631 !important;
        color: #FFFFFF !important;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #FFFFFF !important;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(20, 54, 37, 0.08);
        border-left: 6px solid #1E5631 !important;
        border-top: 1px solid #DCE5DC !important;
        border-right: 1px solid #DCE5DC !important;
        border-bottom: 1px solid #DCE5DC !important;
        margin-bottom: 15px;
    }
    .metric-card h4 {
        color: #4A6B58 !important;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .metric-card h2 {
        color: #143625 !important;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .metric-card p {
        color: #2E6F40 !important;
        font-size: 13px;
        margin: 0;
    }

    /* Info Boxes */
    .info-box {
        background-color: #EDF3ED !important;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #C8D9C8 !important;
        border-left: 5px solid #2E8F40 !important;
        margin-bottom: 15px;
    }
    .info-box h4 {
        color: #143625 !important;
        margin-top: 0;
    }

    /* Catchy Grid Alert Box */
    .grid-alert {
        background-color: #FFF3CD !important;
        border: 1px solid #FFEEBA !important;
        border-left: 6px solid #856404 !important;
        padding: 16px;
        border-radius: 8px;
        color: #856404 !important;
        font-weight: 600;
        margin-bottom: 20px;
    }

    /* GREEN BUTTON WITH PERMANENT WHITE TEXT */
    .stButton > button, .stDownloadButton > button {
        background-color: #1E5631 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #143625 !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    .stButton > button *, .stDownloadButton > button * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #143625 !important;
        color: #FFFFFF !important;
    }

    /* CLEAN TABLES (NO HEAVY OUTER BOX BORDER) */
    [data-testid="stTable"], [data-testid="stTable"] table, table {
        border: none !important;
        border-collapse: collapse !important;
        background-color: #FFFFFF !important;
        margin-top: 10px !important;
        margin-bottom: 20px !important;
    }
    [data-testid="stTable"] th, [data-testid="stTable"] td, th, td {
        border: 1px solid #C8D9C8 !important;
        color: #000000 !important;
        background-color: #FFFFFF !important;
        padding: 10px !important;
    }
    [data-testid="stTable"] th, th {
        background-color: #E3EDE3 !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }
    [data-testid="stDataFrame"] {
        border: none !important;
        border-radius: 6px !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR: LANGUAGE SELECTOR & QR CODE ---
with st.sidebar:
  try:
    st.image("liwa_logo.png", width=180)
  except Exception:
    st.markdown(
        "<div style='background: white; padding: 10px; border-radius: 8px;"
        " text-align: center; color: #143625 !important; font-weight:"
        " bold;'>[Liwa University Logo]</div>",
        unsafe_allow_html=True,
    )

  st.markdown("---")
  lang = st.selectbox("🌐 Language / اللغة", ["English", "العربية (Arabic)"])
  st.markdown("---")

  # DYNAMIC QR CODE SECTION IN SIDEBAR
  if lang == "English":
    st.markdown("### 📱 Live Web App")
    st.markdown("Scan to open dashboard:")
  else:
    st.markdown("### 📱 التطبيق المباشر")
    st.markdown("امسح الرمز لفتح المنصة:")

  dashboard_url = "https://ecosmart-campus-hackathon26.streamlit.app"

  dash_qr = qrcode.QRCode(version=1, box_size=5, border=2)
  dash_qr.add_data(dashboard_url)
  dash_qr.make(fit=True)
  dash_img = dash_qr.make_image(fill_color="#F7F9F6", back_color="#143625")

  buf_dash = io.BytesIO()
  dash_img.save(buf_dash, format="PNG")

  st.image(buf_dash.getvalue(), width=140)

# --- FULL BILINGUAL DICTIONARY (ALL 7 TABS) ---
TEXT = {
    "English": {
        "title": "🌿 EcoSmart Campus : Next-Gen Resource & Experience Hub",
        "subtitle": (
            "Unifying Passive Cooling, AI Predictive HVAC, Wireless IoT"
            " Automation & Student Eco-Rewards"
        ),
        "header_team": (
            "<strong>Project Team:</strong> Fathima Faseeha Faizoor & Shivani"
            " Sruthi Soorjith | <strong>Supervisor:</strong> Dr. Karamath Ateeq"
            " <em>(Dept. of Engineering & Computing)</em>"
        ),
        "header_sdgs": "<strong>UN SDGs:</strong> 9, 11 & 12",
        "tabs": [
            "📊 Executive Command Center",
            "🤖 AI Predictive HVAC & Anomaly Lab",
            "⚡ Energy3D Thermal & Solar Lab",
            "📱 Student Eco-Rewards & QR Hub",
            "💰 Financial ROI & Scenario Engine",
            "🛠️ ESP32 Hardware & Retrofit BOM",
            "🌍 UN SDGs & UAE Net Zero 2050",
        ],
        # TAB 1
        "t1_sub": "🚀 Campus-Wide Annual Impact & Real-World Scale",
        "t1_k1_t": "Energy Saved & Generated",
        "t1_k1_s": "<b>Real-Life Scale:</b> ≈ Powering 35 UAE homes for a full year",
        "t1_k2_t": "CO₂ Emissions Avoided",
        "t1_k2_s": (
            "<b>Real-Life Scale:</b> ≈ Taking 50 cars off Abu Dhabi roads"
            " annually"
        ),
        "t1_k3_t": "Landscaping Water Saved",
        "t1_k3_s": "<b>Real-Life Scale:</b> ≈ Filling 3.5 Olympic swimming pools",
        "t1_k4_t": "Landfill Waste Diverted",
        "t1_k4_s": (
            "<b>Real-Life Scale:</b> ≈ 18 full garbage trucks diverted per year"
        ),
        "t1_tel_h": "🏢 Live Zone-by-Zone Campus Telemetry & ESP32 Status",
        "t1_toggle": (
            "🎛️ Simulate Students Leaving Engineering Building A (Test Live"
            " ESP32 Relay Cutoff)"
        ),
        "t1_toggle_msg": (
            "⚡ ESP32 PIR Sensor detected 0 occupancy for >5 mins in"
            " Engineering Building A -> Relay triggered AUTOMATIC AC CUTOFF"
            " (12.4 kW saved instantaneously)!"
        ),
        "csv_btn": "📥 Download Executive Campus Telemetry Report (CSV)",
        "t1_mat_h": "🔥 Hot-Climate Challenge vs. EcoSmart Architectural Solution",
        # TAB AI
        "ai_header": (
            "🤖 AI Predictive Pre-Cooling & Anomaly Detection Engine"
            " (Random Forest + Isolation Forest)"
        ),
        "ai_desc": (
            "Trained on Abu Dhabi ambient temperature, solar irradiance, and"
            " Liwa University class schedules to forecast next-24-hour HVAC"
            " demand and detect equipment faults."
        ),
        "ai_sim_title": (
            "🎛️ Live AI Scenario Controls (Test Real-Time Model Inference)"
        ),
        "ai_temp_slider": "Peak Outdoor Ambient Temperature (°C)",
        "ai_occ_slider": "Campus Classroom Occupancy Rate (%)",
        "ai_fault_toggle": (
            "⚠️ Simulate HVAC Compressor / Open-Window Anomaly in Block A"
        ),
        "grid_alert_text": (
            "⚠️ EXTREME HEAT ALERT (>45°C): AI automatically initiated"
            " campus-wide pre-cooling and deferred non-essential EV charging"
            " to stabilize the Abu Dhabi grid!"
        ),
        "ai_kpi1_title": "AI Predicted Peak Cooling",
        "ai_kpi1_sub": "Forecasted via Random Forest Regressor",
        "ai_kpi2_title": "AI Pre-Cooling Shift Savings",
        "ai_kpi2_sub": "Off-peak thermal storage optimization",
        "ai_kpi3_title": "System Anomaly Status",
        "ai_kpi3_normal": "🟢 Normal (99.2% Health)",
        "ai_kpi3_alert": "🔴 Fault Detected (Block A)",
        "ai_kpi3_sub_normal": "Isolation Forest: All zones within baseline",
        "ai_kpi3_sub_alert": "Isolation Forest: +42% abnormal kW draw!",
        "ai_chart_title": (
            "AI 24-Hour Cooling Load Forecast vs. Smart Pre-Cooling Schedule"
        ),
        "ai_action_header": (
            "⚡ Automated AI Control & Optimization Actions (ESP32 Relay"
            " Commands)"
        ),
        "ai_col_zone": "Campus Zone",
        "ai_col_pred": "AI Forecasted Load (kW)",
        "ai_col_action": "Automated AI Action",
        "ai_col_status": "ESP32 Relay State",
        # TAB 2
        "t2_sub": (
            "☀️ Abu Dhabi May 2 Hourly Cooling & Solar Load Simulation"
            " (Energy3D)"
        ),
        "t2_chart": (
            "24-Hour Energy3D Simulation: Thermal Cooling vs. Solar Generation"
            " (May 2)"
        ),
        "t2_b1_h": "🏛️ Architectural Passive Shading Insights",
        "t2_b1_li": """
            <li><b>Peak Solar Window:</b> Intense solar radiation hits between 7 AM and 5 PM in Abu Dhabi.</li>
            <li><b>Glazing Optimization:</b> Reducing window span from 5×3 m to 3×1 m with angled louvers cuts peak cooling demand from <b>18 kW to 13 kW (−28%)</b>.</li>
            <li><b>Daylight Preservation:</b> Soft ambient daylight (~7,500 kWh/yr saved) is retained without glare.</li>
        """,
        "t2_b2_h": "⚡ Solar Canopy Generation Metrics",
        "t2_b2_li": """
            <li><b>Capacity:</b> 375 kWp solar canopy spanning 150 parking spaces.</li>
            <li><b>Annual Yield:</b> Generates 540,000 kWh/yr of clean renewable electricity.</li>
            <li><b>Microclimate Benefit:</b> Lowers ambient parking temperatures, protecting parked student and faculty vehicles from extreme heat.</li>
        """,
        # TAB 3
        "t3_sub": "📱 Gamified Smart Recycling & QR Eco-Credit Generator",
        "t3_c1_h": "### Generate Student Eco-Reward QR Code",
        "t3_id": "Enter Liwa Student ID",
        "t3_name": "Student Name",
        "t3_bin": "Recycling Station",
        "t3_waste": "Waste Deposited",
        "t3_btn": "Generate Secure QR Token",
        "t3_cap": "Scan at Liwa Cafeteria Kiosk for Perks!",
        "t3_ok": (
            "QR Token Generated! Redeemable for cafeteria coffee & meal"
            " discounts."
        ),
        "t3_c2_h": "### Live Smart Bin Telemetry & Fill Levels",
        "t3_cat_h": "### 🍔 Cafeteria Perks & Redemption Catalog",
        "t3_cat_li": """
            <li><b>☕ 100 Eco-Credits:</b> Free Specialty Coffee at Liwa Campus Café</li>
            <li><b>🥪 250 Eco-Credits:</b> 20% Discount on Healthy Lunch Meals</li>
            <li><b>🅿️ 500 Eco-Credits:</b> Reserved Shaded Solar Parking Slot for 1 Month</li>
            <li><b>📚 1,000 Eco-Credits:</b> Bookstore Voucher for Engineering Textbooks</li>
        """,
        # TAB 4
        "t4_sub": "💵 CapEx vs. Utility Payback & 10-Year Scenario Modeling",
        "t4_desc": (
            "Use the interactive sliders below to model Liwa University's"
            " capital expenditure, electricity tariff rates, and long-term"
            " financial returns."
        ),
        "t4_s1": "Total CapEx Investment (AED)",
        "t4_s2": "Electricity Tariff (AED / kWh)",
        "t4_k1_t": "Annual Utility Savings",
        "t4_k1_s": "Based on 568,500 kWh annual impact",
        "t4_k2_t": "Simple Payback Period",
        "t4_k2_v": "Years",
        "t4_k2_s": "Rapid return on green infrastructure",
        "t4_k3_t": "10-Year Net Cumulative Savings",
        "t4_k3_s": "Post-CapEx operational net gain",
        "impact_badge_title": "🌱 Live Student-Scaled Sustainability Impact Badge",
        "impact_slider": "Active Student Population Scale",
        "road_h": "### 🗺️ 3-Phase Campus Rollout & Feasibility Roadmap",
        # TAB 5
        "t5_sub": "🛠️ Non-Invasive ESP32 Retrofit Architecture & GPIO Pinout BOM",
        "t5_desc": (
            "EcoSmart is designed for **zero wall rewiring**, utilizing wireless"
            " ESP32 microcontrollers deployed modularly across existing campus"
            " infrastructure."
        ),
        # TAB 6
        "t6_sub": "🌍 Strategic Alignment: UN SDGs & UAE Net Zero 2050",
        "t6_sdg1": (
            "<h4>🎯 UN SDG 9</h4><h3>Industry, Innovation &"
            " Infrastructure</h3><p>Deploying non-invasive IoT retrofits,"
            " ESP32 microcontrollers, and digital twin analytics across Liwa"
            " University with zero structural disruption.</p>"
        ),
        "t6_sdg2": (
            "<h4>🏙️ UN SDG 11</h4><h3>Sustainable Cities &"
            " Communities</h3><p>Optimizing campus resource efficiency,"
            " cutting 227.4 tons of annual CO₂ emissions, and fostering an"
            " active sustainability culture.</p>"
        ),
        "t6_sdg3": (
            "<h4>♻️ UN SDG 12</h4><h3>Responsible Consumption &"
            " Production</h3><p>Tripling waste recycling diversion from 15% to"
            " 45% via gamified smart bins and reducing landscaping irrigation"
            " water use by 30%.</p>"
        ),
        "t6_uae_h": "### 🇦🇪 Contribution to UAE Net Zero 2050 Strategic Initiative",
        "t6_uae_li": """
            <li><b>Decarbonization of Educational Campuses:</b> Direct reduction of energy consumption through passive window glazing optimization and automated HVAC scheduling.</li>
            <li><b>Renewable Energy Integration:</b> 375 kWp solar canopy installation generating 540,000 kWh/yr of clean renewable electricity, directly decreasing reliance on grid fossil fuels.</li>
            <li><b>Water Security in Arid Climates:</b> Smart soil-moisture sensors and weather-linked scheduling save 8,760 m³ of landscaping water annually, supporting UAE water conservation targets.</li>
            <li><b>Bilingual Arabic/English Accessibility:</b> Ensuring seamless deployment and adoption across national and international academic institutions in the UAE.</li>
        """,
    },
    "العربية (Arabic)": {
        "title": "🌿 حرم إيكوسمارت الذكي : مركز الموارد والاستدامة المتكامل",
        "subtitle": (
            "التبريد السلبي، وأتمتة إنترنت الأشياء، وتحسين الذكاء الاصطناعي للتكييف"
            " ومكافآت الطلاب"
        ),
        "header_team": (
            "<strong>فريق العمل:</strong> فاطمة فصيحة فيزور وشيفاني سروثي"
            " سورجيث | <strong>المشرف الأكاديمي:</strong> د. كرامات عتيق"
            " <em>(قسم الهندسة والحوسبة)</em>"
        ),
        "header_sdgs": "<strong>أهداف التنمية المستدامة:</strong> 9، 11 و 12",
        "tabs": [
            "📊 مركز القيادة التنفيذي",
            "🤖 مختبر الذكاء الاصطناعي للتكييف وكشف الأعطال",
            "⚡ مختبر المحاكاة الحرارية والطاقة الشمسية",
            "📱 مركز مكافآت الطلاب وإعادة التدوير",
            "💰 محرك العائد المالي والجدوى",
            "🛠️ عتاد ESP32 ومخطط التوصيل",
            "🌍 أهداف التنمية المستدامة وحياد الإمارات 2050",
        ],
        # TAB 1 (ARABIC)
        "t1_sub": (
            "🚀 الأثر السنوي الشامل على مستوى الحرم الجامعي والمقياس الواقعي"
        ),
        "t1_k1_t": "الطاقة الموفرة والمولدة سنوياً",
        "t1_k1_s": (
            "<b>المقياس الواقعي:</b> ≈ تزويد 35 منزلاً إماراتياً بالكهرباء لمدة"
            " عام كامل"
        ),
        "t1_k2_t": "انبعاثات ثاني أكسيد الكربون المتجنبة",
        "t1_k2_s": (
            "<b>المقياس الواقعي:</b> ≈ إزالة 50 سيارة من شوارع أبوظبي سنوياً"
        ),
        "t1_k3_t": "مياه الري الموفرة سنوياً",
        "t1_k3_s": "<b>المقياس الواقعي:</b> ≈ ملء 3.5 مسابح أولمبية بالكامل",
        "t1_k4_t": "النفايات المحولة عن المكبات",
        "t1_k4_s": "<b>المقياس الواقعي:</b> ≈ تقليل 18 شاحنة نفايات ممتلئة سنوياً",
        "t1_tel_h": "🏢 القياس عن بُعد المباشر لمناطق الحرم الجامعي وحالة ESP32",
        "t1_toggle": (
            "🎛️ محاكاة مغادرة الطلاب لمبنى الهندسة (أ) (اختبار الفصل التلقائي"
            " لمرحل ESP32)"
        ),
        "t1_toggle_msg": (
            "⚡ رصد مستشعر الحركة ESP32 خلو مبنى الهندسة (أ) لأكثر من 5 دقائق"
            " -> تم تفعيل الفصل التلقائي للتكييف (توفير فوري بمقدار 12.4"
            " كيلوواط)!"
        ),
        "csv_btn": "📥 تحميل تقرير القياسات التنفيذي للحرم الجامعي (CSV)",
        "t1_mat_h": (
            "🔥 تحديات المناخ الحار مقابل حلول إيكوسمارت المعمارية والذكية"
        ),
        # TAB AI (ARABIC)
        "ai_header": (
            "🤖 محرك الذكاء الاصطناعي للتبريد الاستباقي وكشف الأعطال"
            " (Random Forest + Isolation Forest)"
        ),
        "ai_desc": (
            "نموذج تعلم آلي مُدرَّب على بيانات الطقس في أبوظبي وجداول المحاضرات"
            " في جامعة ليوا للتنبؤ بأحمال التكييف خلال 24 ساعة واكتشاف الهدر"
            " تلقائياً."
        ),
        "ai_sim_title": (
            "🎛️ محاكاة الذكاء الاصطناعي المباشرة (اختبار التنبؤ الفوري)"
        ),
        "ai_temp_slider": "ذروة درجة الحرارة الخارجية في أبوظبي (°م)",
        "ai_occ_slider": "نسبة إشغال القاعات الدراسية في الحرم الجامعي (%)",
        "ai_fault_toggle": (
            "⚠️ محاكاة عطل في ضاغط التكييف أو نافذة مفتوحة (مبنى أ)"
        ),
        "grid_alert_text": (
            "⚠️ تنبيه حرارة شديدة (>45°م): قام الذكاء الاصطناعي تلقائياً بتفعيل"
            " التبريد الاستباقي وتأجيل شحن السيارات الكهربائية غير الضروري"
            " لحماية شبكة أبوظبي الكهربائية!"
        ),
        "ai_kpi1_title": "ذروة التبريد المتوقعة (AI)",
        "ai_kpi1_sub": "تنبؤ عبر خوارزمية الغابة العشوائية",
        "ai_kpi2_title": "وفورات التبريد الاستباقي الذكي",
        "ai_kpi2_sub": "نقل الأحمال الحرارية خارج أوقات الذروة",
        "ai_kpi3_title": "حالة كشف الأعطال الذكي",
        "ai_kpi3_normal": "🟢 طبيعي (كفاءة 99.2%)",
        "ai_kpi3_alert": "🔴 تم رصد عطل (مبنى أ)",
        "ai_kpi3_sub_normal": "جميع المناطق تعمل ضمن المعدل الطبيعي",
        "ai_kpi3_sub_alert": "استهلاك طاقة غير طبيعي (+42% فوق المتوقع)!",
        "ai_chart_title": (
            "توقعات الذكاء الاصطناعي لأحمال التبريد (24 ساعة) مقابل جدول"
            " التبريد الاستباقي"
        ),
        "ai_action_header": (
            "⚡ إجراءات التحكم والتحسين التلقائية (أوامر متحكمات ESP32)"
        ),
        "ai_col_zone": "منطقة الحرم الجامعي",
        "ai_col_pred": "الحمل المتوقع (كيلوواط)",
        "ai_col_action": "إجراء الذكاء الاصطناعي التلقائي",
        "ai_col_status": "حالة مرحّل ESP32",
        # TAB 2 (ARABIC)
        "t2_sub": (
            "☀️ محاكاة أحمال التبريد والطاقة الشمسية في أبوظبي ليوم 2 مايو"
            " (Energy3D)"
        ),
        "t2_chart": (
            "محاكاة 24 ساعة: التبريد الحراري مقابل توليد الطاقة الشمسية (2 مايو)"
        ),
        "t2_b1_h": "🏛️ رؤى التظليل السلبي والتصميم المعماري",
        "t2_b1_li": """
            <li><b>ذروة الإشعاع الشمسي:</b> تبلغ ذروة الحرارة الشمسية بين الساعة 7 صباحاً و5 مساءً في أبوظبي.</li>
            <li><b>تحسين النوافذ الزجاجية:</b> تقليص أبعاد النوافذ من 5×3 م إلى 3×1 م مع كاسرات شمسية يخفض ذروة التبريد من <b>18 إلى 13 كيلوواط (−28%)</b>.</li>
            <li><b>الحفاظ على الإضاءة الطبيعية:</b> توفير إضاءة نهارية مريحة (~7,500 كيلوواط ساعة/سنة) دون وهج حراري.</li>
        """,
        "t2_b2_h": "⚡ مؤشرات توليد المظلات الشمسية للمواقف",
        "t2_b2_li": """
            <li><b>السعة الإنتاجية:</b> مظلات شمسية بقدرة 375 كيلوواط ذروة تغطي 150 موقف سيارة.</li>
            <li><b>الإنتاج السنوي:</b> توليد 540,000 كيلوواط ساعة/سنة من الكهرباء النظيفة المتجددة.</li>
            <li><b>تحسين المناخ المحلي:</b> خفض حرارة مواقف السيارات وحماية مركبات الطلاب وأعضاء هيئة التدريس.</li>
        """,
        # TAB 3 (ARABIC)
        "t3_sub": (
            "📱 نظام إعادة التدوير الذكي ومولد رموز المكافآت الطلابية (QR)"
        ),
        "t3_c1_h": "### توليد رمز المكافأة البيئية للطالب (QR)",
        "t3_id": "أدخل الرقم الجامعي للطالب في جامعة ليوا",
        "t3_name": "اسم الطالب",
        "t3_bin": "محطة إعادة التدوير الذكية",
        "t3_waste": "نوع وكمية النفايات المودعة",
        "t3_btn": "توليد رمز QR الآمن للمكافأة",
        "t3_cap": "امسح الرمز في كافتيريا جامعة ليوا للحصول على الخصم!",
        "t3_ok": (
            "تم توليد رمز المكافأة بنجاح! قابل للاستبدال بخصومات القهوة والوجبات."
        ),
        "t3_c2_h": "### القياس المباشر لمستوى امتلاء الحاويات الذكية",
        "t3_cat_h": "### 🍔 كتالوج مكافآت الكافتيريا والحرم الجامعي",
        "t3_cat_li": """
            <li><b>☕ 100 نقطة بيئية:</b> قهوة مختصة مجانية في مقهى حرم جامعة ليوا</li>
            <li><b>🥪 250 نقطة بيئية:</b> خصم 20% على الوجبات الصحية في الكافتيريا</li>
            <li><b>🅿️ 500 نقطة بيئية:</b> موقف سيارة مظلل بالطاقة الشمسية محجوز لمدة شهر</li>
            <li><b>📚 1,000 نقطة بيئية:</b> قسيمة شرائية من مكتبة الجامعة للكتب الهندسية</li>
        """,
        # TAB 4 (ARABIC)
        "t4_sub": (
            "💵 تحليل النفقات الرأسمالية وفترة الاسترداد والعائد لعشر سنوات"
        ),
        "t4_desc": (
            "استخدم أشرطة التمرير التفاعلية أدناه لمحاكاة الاستثمار الرأسمالي"
            " وتعرفة الكهرباء والعوائد المالية طويلة الأجل لجامعة ليوا."
        ),
        "t4_s1": "إجمالي الاستثمار الرأسمالي (درهم إماراتي)",
        "t4_s2": "تعرفة الكهرباء (درهم / كيلوواط ساعة)",
        "t4_k1_t": "الوفورات السنوية في الفواتير",
        "t4_k1_s": "بناءً على أثر سنوي يبلغ 568,500 كيلوواط ساعة",
        "t4_k2_t": "فترة استرداد رأس المال",
        "t4_k2_v": "سنوات",
        "t4_k2_s": "عائد استثماري سريع للبنية التحتية الخضراء",
        "t4_k3_t": "صافي الوفورات التراكمية (10 سنوات)",
        "t4_k3_s": "صافي الربح التشغيلي بعد استرداد رأس المال",
        "impact_badge_title": (
            "🌱 شارة الأثر البيئي الديناميكي (حسب عدد الطلاب)"
        ),
        "impact_slider": "مقياس عدد الطلاب النشطين في الحرم",
        "road_h": "### 🗺️ خارطة طريق التنفيذ والجدوى على 3 مراحل",
        # TAB 5 (ARABIC)
        "t5_sub": "🛠️ معمارية التحديث اللاسلكي ESP32 وجدول توصيل المستشعرات",
        "t5_desc": (
            "تم تصميم نظام إيكوسمارت **دون الحاجة لأي تكسير أو إعادة تمديد"
            " للأسلاك**، باستخدام متحكمات ESP32 اللاسلكية القابلة للتركيب"
            " المباشر."
        ),
        # TAB 6 (ARABIC)
        "t6_sub": (
            "🌍 التوافق الاستراتيجي: أهداف التنمية المستدامة ومبادرة الإمارات"
            " للحياد المناخي 2050"
        ),
        "t6_sdg1": (
            "<h4>🎯 الهدف 9</h4><h3>الصناعة والابتكار والهياكل"
            " الأساسية</h3><p>نشر حلول إنترنت الأشياء اللاسلكية ومتحكمات ESP32"
            " والتوأم الرقمي في جامعة ليوا دون أي تعطيل للبنية التحتية.</p>"
        ),
        "t6_sdg2": (
            "<h4>🏙️ الهدف 11</h4><h3>مدن ومجتمعات محلية مستدامة</h3><p>تحسين"
            " كفاءة موارد الحرم الجامعي، وخفض 227.4 طن من انبعاثات الكربون"
            " سنوياً، وتعزيز ثقافة الاستدامة.</p>"
        ),
        "t6_sdg3": (
            "<h4>♻️ الهدف 12</h4><h3>الاستهلاك والإنتاج المسؤولان</h3><p>مضاعفة"
            " نسبة إعادة التدوير ثلاث مرات من 15% إلى 45% عبر الحاويات الذكية"
            " وتقليل مياه الري بنسبة 30%.</p>"
        ),
        "t6_uae_h": (
            "### 🇦🇪 المساهمة في المبادرة الاستراتيجية للحياد المناخي 2050"
            " لدولة الإمارات"
        ),
        "t6_uae_li": """
            <li><b>إزالة الكربون من المؤسسات التعليمية:</b> خفض مباشر لاستهلاك الطاقة عبر تحسين النوافذ السلبية والجدولة الذكية للتكييف.</li>
            <li><b>دمج الطاقة المتجددة:</b> تركيب مظلات شمسية بقدرة 375 كيلوواط ذروة تنتج 540,000 كيلوواط ساعة/سنة من الكهرباء النظيفة.</li>
            <li><b>الأمن المائي في المناخات الجافة:</b> مستشعرات رطوبة التربة والجدولة الذكية توفر 8,760 متر مكعب من مياه الري سنوياً.</li>
            <li><b>دعم اللغتين العربية والإنجليزية:</b> ضمان سهولة التطبيق والتبني في كافة الجامعات الوطنية والدولية في دولة الإمارات.</li>
        """,
    },
}

t = TEXT[lang]

# --- CLEAN LOGO DISPLAY (NO STRAY BOXES) ---
try:
  st.image("liwa_logo.png", width=220)
except Exception:
  st.markdown(
      "<h3 style='color: #143625; margin:0;'>Liwa University</h3>",
      unsafe_allow_html=True,
  )

st.markdown(
    f"""
    <h1 style="color: #143625 !important; font-size: 34px !important; font-weight: 800 !important; margin-top: 10px; margin-bottom: 6px;">{t['title']}</h1>
    <h3 style="color: #1E3A2F !important; font-size: 19px !important; font-weight: 600 !important; margin-top: 0px; margin-bottom: 12px;">{t['subtitle']}</h3>
    <p style="color: #2E5A44 !important; font-size: 14px !important; margin: 3px 0;">{t['header_team']}</p>
    <p style="color: #2E5A44 !important; font-size: 14px !important; margin: 3px 0 20px 0;">{t['header_sdgs']}</p>
""",
    unsafe_allow_html=True,
)

# --- TOP NAVIGATION TABS ---
tab1, tab_ai, tab2, tab3, tab4, tab5, tab6 = st.tabs(t["tabs"])

# ==========================================
# TAB 1: EXECUTIVE COMMAND CENTER
# ==========================================
with tab1:
  st.subheader(t["t1_sub"])

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>{t['t1_k1_t']}</h4>
                <h2>568,500 kWh</h2>
                <p>{t['t1_k1_s']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>{t['t1_k2_t']}</h4>
                <h2>227.4 Tons</h2>
                <p>{t['t1_k2_s']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>{t['t1_k3_t']}</h4>
                <h2>8,760 m³</h2>
                <p>{t['t1_k3_s']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>{t['t1_k4_t']}</h4>
                <h2>109.5 Tons</h2>
                <p>{t['t1_k4_s']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown(f"### {t['t1_tel_h']}")

  # LIVE INTERACTIVE ESP32 CONTROL & OPTIMIZE TOGGLE
  simulate_vacant = st.toggle(t["t1_toggle"], value=False)
  if simulate_vacant:
    st.success(t["t1_toggle_msg"])

  if lang == "English":
    eng_occ = (
        "Vacant (ESP32 Relay Cutoff Active)"
        if simulate_vacant
        else "Occupied (42 students)"
    )
    eng_hvac = "0.0 kW (Saved)" if simulate_vacant else "12.4 kW"
    eng_health = (
        "🟡 Eco-Cutoff Triggered" if simulate_vacant else "🟢 Online"
    )

    zones_df = pd.DataFrame({
        "Campus Zone": [
            "Engineering Building A",
            "Library Atrium Hub",
            "Science Labs Block",
            "Student Activity Center",
            "Admin & Faculty Tower",
            "Parking Canopy Solar Array",
        ],
        "Occupancy Status": [
            eng_occ,
            "Occupied (85 students)",
            "Vacant (AC Cutoff Active)",
            "Occupied (120 students)",
            "Vacant (Eco-Mode)",
            "Active Generation (375 kWp)",
        ],
        "Indoor Air Quality (CO₂)": [
            "430 ppm (Fresh)" if simulate_vacant else "650 ppm (Fresh)",
            "780 ppm (Good)",
            "410 ppm (Fresh)",
            "920 ppm (Acceptable)",
            "500 ppm (Fresh)",
            "N/A (Outdoor)",
        ],
        "HVAC Load (kW)": [
            eng_hvac,
            "18.2 kW",
            "0.0 kW (Saved)",
            "22.5 kW",
            "8.1 kW",
            "-145 kW (Net Export)",
        ],
        "System Health": [
            eng_health,
            "🟢 Online",
            "🟢 Online",
            "🟢 Online",
            "🟢 Online",
            "☀️ Peak Generating",
        ],
    })
  else:
    eng_occ = (
        "شاغر (تم فصل التكييف تلقائياً عبر ESP32)"
        if simulate_vacant
        else "مشغول (42 طالباً)"
    )
    eng_hvac = "0.0 كيلوواط (تم التوفير)" if simulate_vacant else "12.4 كيلوواط"
    eng_health = (
        "🟡 وضع التوفير نشط" if simulate_vacant else "🟢 متصل ويعمل"
    )

    zones_df = pd.DataFrame({
        "منطقة الحرم الجامعي": [
            "مبنى الهندسة (أ)",
            "بهو المكتبة الرئيسية",
            "مبنى مختبرات العلوم",
            "مركز الأنشطة الطلابية",
            "برج الإدارة وأعضاء هيئة التدريس",
            "مظلات مواقف السيارات الشمسية",
        ],
        "حالة الإشغال": [
            eng_occ,
            "مشغول (85 طالباً)",
            "شاغر (تم فصل التكييف)",
            "مشغول (120 طالباً)",
            "شاغر (الوضع الاقتصادي)",
            "توليد نشط (375 كيلوواط ذروة)",
        ],
        "جودة الهواء الداخلي (CO₂)": [
            "430 ppm (نقي)" if simulate_vacant else "650 ppm (نقي)",
            "780 ppm (جيد)",
            "410 ppm (نقي)",
            "920 ppm (مقبول)",
            "500 ppm (نقي)",
            "غير منطبق (خارجي)",
        ],
        "حمل التكييف (كيلوواط)": [
            eng_hvac,
            "18.2 كيلوواط",
            "0.0 كيلوواط (تم التوفير)",
            "22.5 كيلوواط",
            "8.1 كيلوواط",
            "-145 كيلوواط (تصدير صافي)",
        ],
        "حالة النظام": [
            eng_health,
            "🟢 متصل ويعمل",
            "🟢 متصل ويعمل",
            "🟢 متصل ويعمل",
            "🟢 متصل ويعمل",
            "☀️ ذروة التوليد الشمسي",
        ],
    })

  st.dataframe(zones_df, use_container_width=True)

  # DOWNLOAD EXECUTIVE REPORT CSV BUTTON
  csv_data = zones_df.to_csv(index=False).encode("utf-8")
  st.download_button(
      label=t["csv_btn"],
      data=csv_data,
      file_name="EcoSmart_Campus_Telemetry_Report.csv",
      mime="text/csv",
  )

  st.markdown(f"### {t['t1_mat_h']}")
  if lang == "English":
    matrix_df = pd.DataFrame({
        "Challenge Domain": [
            "Solar Heat Gain",
            "Empty-Room AC Idle",
            "Landscape Watering",
            "Solid Waste Management",
            "Student Engagement",
        ],
        "Abu Dhabi Baseline Issue": [
            "70%+ cooling share from unshaded 5×3 m windows",
            "AC & lights run continuously in empty lecture halls",
            "Timer-based irrigation wastes 80,000 L/day",
            "Low recycling diversion rate (only 15%)",
            "Zero visibility or incentive for student participation",
        ],
        "EcoSmart Upgrades": [
            "Passive glazing reduction to 3×1 m + overhang louvers (−28% peak)",
            "ESP32 PIR motion & CO₂ nodes cut idle AC (21,000 kWh/yr saved)",
            (
                "Soil moisture probes & weather triggers cut water by 30%"
                " (56,000 L/day)"
            ),
            "Ultrasonic smart bins + QR rewards triple diversion to 45%",
            "QR-linked smart bins award digital credits for cafeteria perks",
        ],
    })
  else:
    matrix_df = pd.DataFrame({
        "مجال التحدي": [
            "اكتساب الحرارة الشمسية",
            "تشغيل التكييف في القاعات الفارغة",
            "ري المسطحات الخضراء",
            "إدارة النفايات الصلبة",
            "مشاركة وتفاعل الطلاب",
        ],
        "المشكلة الحالية في أبوظبي": [
            "أكثر من 70% من حمل التبريد بسبب النوافذ الكبيرة غير المظللة (5×3 م)",
            "استمرار عمل التكييف والإضاءة في القاعات الدراسية الفارغة",
            "الري المؤقت التقليدي يهدر 80,000 لتر يومياً",
            "انخفاض معدل إعادة التدوير (15% فقط)",
            "غياب الحوافز أو المتابعة لمشاركة الطلاب في الاستدامة",
        ],
        "حلول إيكوسمارت الذكية": [
            "تقليص النوافذ إلى 3×1 م مع كاسرات شمسية (خفض الذروة بنسبة 28%)",
            "مستشعرات الحركة ESP32 تفصل التكييف تلقائياً (توفير 21,000 كيلوواط ساعة/سنة)",
            "مستشعرات رطوبة التربة والطقس تخفض المياه بنسبة 30% (56,000 لتر/يوم)",
            "حاويات ذكية بالموجات فوق الصوتية + مكافآت QR ترفع التدوير إلى 45%",
            "منح نقاط رقمية فورية عبر QR لاستبدالها في كافتيريا الجامعة",
        ],
    })
  st.table(matrix_df)

# ==========================================
# TAB AI: AI PREDICTIVE HVAC & ANOMALY LAB
# ==========================================
with tab_ai:
  st.subheader(t["ai_header"])
  st.markdown(t["ai_desc"])

  @st.cache_resource
  def train_hvac_ai_model():
    np.random.seed(42)
    n_samples = 500
    hours_data = np.random.randint(0, 24, n_samples)
    temp_data = np.random.uniform(26, 48, n_samples)
    occ_data = np.random.uniform(0, 100, n_samples)
    cooling_kw = (
        0.35 * np.maximum(0, temp_data - 22)
        + 0.08 * occ_data
        + 4.5 * np.sin(np.pi * np.clip((hours_data - 6) / 14, 0, 1))
        + np.random.normal(0, 0.4, n_samples)
    )
    X_train = pd.DataFrame(
        {"hour": hours_data, "temp": temp_data, "occ": occ_data}
    )
    rf_model = RandomForestRegressor(n_estimators=60, random_state=42)
    rf_model.fit(X_train, cooling_kw)

    iso_model = IsolationForest(contamination=0.05, random_state=42)
    iso_model.fit(X_train.assign(kw=cooling_kw))
    return rf_model, iso_model

  rf_model, iso_model = train_hvac_ai_model()

  st.markdown(f"#### {t['ai_sim_title']}")
  c1, c2, c3 = st.columns([1, 1, 1.2])
  with c1:
    peak_temp = st.slider(t["ai_temp_slider"], 28, 50, 43)
  with c2:
    avg_occ = st.slider(t["ai_occ_slider"], 10, 100, 75)
  with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    inject_fault = st.checkbox(t["ai_fault_toggle"], value=False)

  # EMERGENCY PEAK-LOAD & GRID ALERT SIMULATOR (>45°C)
  if peak_temp > 45:
    st.markdown(
        f'<div class="grid-alert">{t["grid_alert_text"]}</div>',
        unsafe_allow_html=True,
    )

  hours_24 = np.arange(0, 24)
  hourly_temps = peak_temp - 9 * np.cos((hours_24 - 14) * np.pi / 12)
  hourly_occ = np.where(
      (hours_24 >= 8) & (hours_24 <= 18), avg_occ, avg_occ * 0.1
  )

  X_pred = pd.DataFrame(
      {"hour": hours_24, "temp": hourly_temps, "occ": hourly_occ}
  )
  ai_predicted_kw = rf_model.predict(X_pred)

  ai_optimized_kw = ai_predicted_kw * 0.84
  ai_optimized_kw[6:9] *= 1.12
  ai_optimized_kw[19:] *= 0.45

  if inject_fault:
    ai_predicted_kw[11:16] *= 1.42

  peak_sample = pd.DataFrame({
      "hour": [14],
      "temp": [hourly_temps[14]],
      "occ": [hourly_occ[14]],
      "kw": [ai_predicted_kw[14]],
  })
  is_anomaly = (iso_model.predict(peak_sample)[0] == -1) or inject_fault

  k1, k2, k3 = st.columns(3)
  with k1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>{t['ai_kpi1_title']}</h4>
            <h2>{np.max(ai_predicted_kw):.1f} kW</h2>
            <p>{t['ai_kpi1_sub']}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
  with k2:
    saved_pct = (
        (np.sum(ai_predicted_kw) - np.sum(ai_optimized_kw))
        / np.sum(ai_predicted_kw)
    ) * 100
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>{t['ai_kpi2_title']}</h4>
            <h2>-{saved_pct:.1f}%</h2>
            <p>{t['ai_kpi2_sub']}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
  with k3:
    status_val = t["ai_kpi3_alert"] if is_anomaly else t["ai_kpi3_normal"]
    status_sub = (
        t["ai_kpi3_sub_alert"] if is_anomaly else t["ai_kpi3_sub_normal"]
    )
    st.markdown(
        f"""
        <div class="metric-card">
            <h4>{t['ai_kpi3_title']}</h4>
            <h2>{status_val}</h2>
            <p>{status_sub}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

  df_ai_plot = pd.DataFrame({
      "Hour": hours_24,
      "Unoptimized AI Baseline Forecast (kW)": ai_predicted_kw,
      "AI Pre-Cooled & Occupancy-Optimized (kW)": ai_optimized_kw,
  })
  fig_ai = px.area(
      df_ai_plot,
      x="Hour",
      y=[
          "Unoptimized AI Baseline Forecast (kW)",
          "AI Pre-Cooled & Occupancy-Optimized (kW)",
      ],
      color_discrete_sequence=["#B45309", "#1E5631"],
      title=t["ai_chart_title"],
  )
  fig_ai.update_layout(
      plot_bgcolor="#FFFFFF",
      paper_bgcolor="#F7F9F6",
      font=dict(color="#000000", size=13),
      title=dict(font=dict(color="#000000", size=16)),
      xaxis=dict(
          title=dict(font=dict(color="#000000")),
          tickfont=dict(color="#000000"),
          gridcolor="#D0D8D0",
          linecolor="#000000",
      ),
      yaxis=dict(
          title=dict(font=dict(color="#000000")),
          tickfont=dict(color="#000000"),
          gridcolor="#D0D8D0",
          linecolor="#000000",
      ),
      legend=dict(
          orientation="h",
          yanchor="bottom",
          y=1.02,
          xanchor="right",
          x=1,
          font=dict(color="#000000"),
      ),
  )
  st.plotly_chart(fig_ai, use_container_width=True)

  st.markdown(f"#### {t['ai_action_header']}")
  if lang == "English":
    ai_actions_df = pd.DataFrame({
        t["ai_col_zone"]: [
            "Engineering Block A",
            "Library Atrium",
            "Science Labs",
            "Student Hub",
        ],
        t["ai_col_pred"]: [
            f"{ai_optimized_kw[14]:.1f} kW",
            f"{ai_optimized_kw[12]:.1f} kW",
            "0.0 kW",
            f"{ai_optimized_kw[15]:.1f} kW",
        ],
        t["ai_col_action"]: [
            (
                "ALERT: Isolate faulty compressor & notify maintenance"
                if is_anomaly
                else "Pre-cool to 21°C at 7:30 AM using solar peak"
            ),
            "Maintain 23°C eco-setpoint; modulate fresh air damper",
            "Zero occupancy predicted until 2:00 PM -> Full AC Cutoff",
            "Sync cooling ramp-up with 12:00 PM break schedule",
        ],
        t["ai_col_status"]: [
            "🔴 Fault Isolated" if is_anomaly else "🟢 Pre-Cooling Active",
            "🟢 Eco-Modulating",
            "🟡 Relay OFF (Saved)",
            "🟢 AI Scheduled",
        ],
    })
  else:
    ai_actions_df = pd.DataFrame({
        t["ai_col_zone"]: [
            "مبنى الهندسة (أ)",
            "بهو المكتبة الرئيسية",
            "مختبرات العلوم",
            "مركز الأنشطة الطلابية",
        ],
        t["ai_col_pred"]: [
            f"{ai_optimized_kw[14]:.1f} kW",
            f"{ai_optimized_kw[12]:.1f} kW",
            "0.0 kW",
            f"{ai_optimized_kw[15]:.1f} kW",
        ],
        t["ai_col_action"]: [
            (
                "تنبيه: عزل الضاغط المعطل وإرسال إشعار للصيانة فوراً"
                if is_anomaly
                else "تبريد استباقي إلى 21°م الساعة 7:30 صباحاً عبر الطاقة"
                " الشمسية"
            ),
            "تثبيت الحرارة عند 23°م وضبط التهوية حسب نسبة ثاني أكسيد الكربون",
            "لا توجد محاضرات متوقعة حتى 2:00 ظهراً -> إيقاف التكييف بالكامل",
            "مزامنة التبريد تلقائياً مع جدول استراحة الطلاب الساعة 12:00 ظهراً",
        ],
        t["ai_col_status"]: [
            "🔴 تم عزل العطل" if is_anomaly else "🟢 تبريد استباقي نشط",
            "🟢 وضع التوفير الذكي",
            "🟡 مغلق تلقائياً (توفير)",
            "🟢 مجدول بالذكاء الاصطناعي",
        ],
    })

  st.dataframe(ai_actions_df, use_container_width=True)

# ==========================================
# TAB 2: ENERGY3D THERMAL & SOLAR LAB
# ==========================================
with tab2:
  st.subheader(t["t2_sub"])

  hours = np.arange(0, 24)
  baseline_cooling = np.array([
      0.5, 0.6, 0.8, 1.2, 1.8, 2.8, 11.0, 16.0, 18.0, 18.8, 18.5, 17.2,
      16.8, 18.3, 18.9, 18.3, 16.8, 13.0, 4.5, 2.0, 1.5, 1.1, 0.8, 0.6,
  ])
  optimized_cooling = baseline_cooling * 0.72
  solar_generation = (
      np.array([
          0, 0, 0, 0, 0, 0.5, 3.5, 7.5, 11.0, 13.0, 12.0, 10.5,
          10.5, 12.0, 13.0, 12.5, 9.5, 4.0, 0.8, 0, 0, 0, 0, 0,
      ])
      * 3.75
  )

  df_energy = pd.DataFrame({
      "Hour": hours,
      "Baseline AC Load (kW) (5×3 m Windows)": baseline_cooling,
      "Optimized AC Load (kW) (3×1 m + Louvers)": optimized_cooling,
      "Solar Canopy Generation (kW)": solar_generation,
  })

  fig = px.line(
      df_energy,
      x="Hour",
      y=[
          "Baseline AC Load (kW) (5×3 m Windows)",
          "Optimized AC Load (kW) (3×1 m + Louvers)",
          "Solar Canopy Generation (kW)",
      ],
      markers=True,
      color_discrete_sequence=["#B45309", "#143625", "#2E8B57"],
      labels={
          "value": "Power (kW or kWh/h)",
          "Hour": "Hour of Day (Abu Dhabi Solar Curve)",
      },
      title=t["t2_chart"],
  )
  fig.update_layout(
      plot_bgcolor="#FFFFFF",
      paper_bgcolor="#F7F9F6",
      font=dict(color="#000000", size=13),
      title=dict(font=dict(color="#000000", size=16)),
      xaxis=dict(
          title=dict(font=dict(color="#000000")),
          tickfont=dict(color="#000000"),
          gridcolor="#D0D8D0",
          linecolor="#000000",
      ),
      yaxis=dict(
          title=dict(font=dict(color="#000000")),
          tickfont=dict(color="#000000"),
          gridcolor="#D0D8D0",
          linecolor="#000000",
      ),
      legend=dict(
          orientation="h",
          yanchor="bottom",
          y=1.02,
          xanchor="right",
          x=1,
          font=dict(color="#000000"),
      ),
  )
  st.plotly_chart(fig, use_container_width=True)

  col1, col2 = st.columns(2)
  with col1:
    st.markdown(
        f"""
            <div class="info-box">
                <h4>{t['t2_b1_h']}</h4>
                <ul>{t['t2_b1_li']}</ul>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f"""
            <div class="info-box">
                <h4>{t['t2_b2_h']}</h4>
                <ul>{t['t2_b2_li']}</ul>
            </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# TAB 3: STUDENT ECO-REWARDS & QR HUB
# ==========================================
with tab3:
  st.subheader(t["t3_sub"])

  col1, col2 = st.columns(2)
  with col1:
    st.markdown(t["t3_c1_h"])
    student_id = st.text_input(t["t3_id"], value="LU-2026-9921")
    student_name = st.text_input(t["t3_name"], value="Fathima Faseeha Faizoor")
    bin_location = st.selectbox(
        t["t3_bin"],
        [
            "Engineering Building - Smart Bin #1 (PET Plastics)",
            "Library Atrium - Smart Bin #2 (Aluminum Cans)",
            "Student Hub - Smart Bin #3 (Office Paper)",
        ],
    )
    waste_type = st.selectbox(
        t["t3_waste"],
        [
            "PET Bottle (0.5 kg) - 25 Credits",
            "Aluminum Can (0.3 kg) - 35 Credits",
            "Mixed Paper (1.2 kg) - 50 Credits",
        ],
    )

    if st.button(t["t3_btn"]):
      qr_payload = f"LiwaEcoSmart:ID={student_id}|Name={student_name}|Bin={bin_location}|Type={waste_type}"
      qr = qrcode.QRCode(version=1, box_size=8, border=2)
      qr.add_data(qr_payload)
      qr.make(fit=True)
      img = qr.make_image(fill_color="#143625", back_color="#F7F9F6")
      buf = io.BytesIO()
      img.save(buf, format="PNG")
      byte_im = buf.getvalue()

      st.image(byte_im, width=220, caption=t["t3_cap"])
      st.success(t["t3_ok"])

  with col2:
    st.markdown(t["t3_c2_h"])
    if lang == "English":
      bins_status_df = pd.DataFrame({
          "Bin ID & Location": [
              "BIN-ENG-01 (Ground Lobby)",
              "BIN-LIB-02 (Reading Hall)",
              "BIN-CAF-03 (Food Court)",
              "BIN-SCI-04 (Chemistry Dept)",
          ],
          "Material Type": [
              "Plastics (PET)",
              "Aluminum Cans",
              "Organic / Mixed",
              "Paper & Cardboard",
          ],
          "Ultrasonic Fill Level": ["78%", "92% (Warning)", "45%", "62%"],
          "Status": ["Normal", "Collection Required", "Normal", "Normal"],
          "Total Diverted (kg/wk)": ["340 kg", "210 kg", "450 kg", "180 kg"],
      })
    else:
      bins_status_df = pd.DataFrame({
          "رمز وموقع الحاوية": [
              "BIN-ENG-01 (بهو الهندسة)",
              "BIN-LIB-02 (قاعة المكتبة)",
              "BIN-CAF-03 (ساحة الطعام)",
              "BIN-SCI-04 (قسم الكيمياء)",
          ],
          "نوع المادة": [
              "بلاستيك (PET)",
              "علب ألمنيوم",
              "نفايات عضوية / مختلطة",
              "ورق وكرتون",
          ],
          "نسبة الامتلاء (فوق صوتي)": ["78%", "92% (تنبيه)", "45%", "62%"],
          "الحالة": ["طبيعي", "مطلوب تفريغ", "طبيعي", "طبيعي"],
          "إجمالي التدوير (كجم/أسبوع)": ["340 كجم", "210 كجم", "450 كجم", "180 كجم"],
      })
    st.dataframe(bins_status_df, use_container_width=True)

    st.markdown(t["t3_cat_h"])
    st.markdown(
        f"""
            <div class="info-box">
                <ul>{t['t3_cat_li']}</ul>
            </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# TAB 4: FINANCIAL ROI & SCENARIO ENGINE
# ==========================================
with tab4:
  st.subheader(t["t4_sub"])
  st.markdown(t["t4_desc"])

  col_s1, col_s2 = st.columns(2)
  with col_s1:
    capex_input = st.slider(
        t["t4_s1"],
        min_value=100000,
        max_value=500000,
        value=220000,
        step=10000,
    )
  with col_s2:
    tariff_input = st.slider(
        t["t4_s2"],
        min_value=0.30,
        max_value=0.70,
        value=0.45,
        step=0.05,
    )

  annual_kwh = 568500
  annual_savings_aed = annual_kwh * tariff_input
  payback_period = capex_input / annual_savings_aed
  net_10yr_savings = (annual_savings_aed * 10) - capex_input

  col_m1, col_m2, col_m3 = st.columns(3)
  with col_m1:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>{t['t4_k1_t']}</h4>
                <h2>AED {annual_savings_aed:,.0f}</h2>
                <p>{t['t4_k1_s']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_m2:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>{t['t4_k2_t']}</h4>
                <h2>{payback_period:.2f} {t['t4_k2_v']}</h2>
                <p>{t['t4_k2_s']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_m3:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>{t['t4_k3_t']}</h4>
                <h2>AED {net_10yr_savings:,.0f}</h2>
                <p>{t['t4_k3_s']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("---")
  st.markdown(f"### {t['impact_badge_title']}")
  student_slider = st.slider(
      t["impact_slider"], min_value=1000, max_value=10000, value=3500, step=500
  )

  scale_factor = student_slider / 3500
  trees_planted = int(12500 * scale_factor)
  olympic_pools = 3.5 * scale_factor

  col_b1, col_b2, col_b3 = st.columns(3)
  with col_b1:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>🌲 Abu Dhabi Mangrove Offset</h4>
                <h2>{trees_planted:,} Trees</h2>
                <p>Equivalent CO₂ absorption per year</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_b2:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>🏊 Water Conservation</h4>
                <h2>{olympic_pools:.1f} Pools</h2>
                <p>Olympic pools of water saved annually</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_b3:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>🎓 Campus Community Impact</h4>
                <h2>{student_slider:,} Students</h2>
                <p>Actively engaged in net-zero rewards</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown(t["road_h"])
  if lang == "English":
    roadmap_df = pd.DataFrame({
        "Rollout Phase": [
            "Phase 1: Quick-Win Pilot",
            "Phase 2: Student Engagement",
            "Phase 3: Campus-Wide Scale",
        ],
        "Strategic Focus": [
            "Wireless IoT Sensor Retrofit",
            "Bilingual UI & Smart Bins",
            "Solar Canopies & AI HVAC",
        ],
        "Key Actions": [
            (
                "Deploy wireless ESP32 occupancy/IAQ nodes & soil moisture"
                " sensors in 1 building; replace estimates with live"
                " telemetry."
            ),
            (
                "Launch bilingual Arabic/English dashboard & QR-linked smart"
                " bins with campus cafeteria eco-rewards."
            ),
            (
                "Reinvest operational utility savings into 375 kWp parking"
                " solar canopies & AI predictive HVAC scheduling."
            ),
        ],
        "Timeline": ["Months 1 - 3", "Months 4 - 6", "Months 7 - 12+"],
    })
  else:
    roadmap_df = pd.DataFrame({
        "مرحلة التنفيذ": [
            "المرحلة 1: التشغيل التجريبي السريع",
            "المرحلة 2: تفاعل الطلاب والاستدامة",
            "المرحلة 3: التوسع الشامل في الحرم",
        ],
        "التركيز الاستراتيجي": [
            "تحديث المستشعرات اللاسلكية (IoT)",
            "الواجهة ثنائية اللغة والحاويات الذكية",
            "المظلات الشمسية والتكييف بالذكاء الاصطناعي",
        ],
        "الإجراءات الرئيسية": [
            "نشر عقد ESP32 اللاسلكية ومستشعرات رطوبة التربة في مبنى واحد واستبدال التقديرات ببيانات حية.",
            "إطلاق لوحة التحكم بالعربية والإنجليزية وربط الحاويات الذكية بمكافآت الكافتيريا.",
            "إعادة استثمار الوفورات المالية في تركيب مظلات شمسية 375 كيلوواط وجدولة التكييف الذكية.",
        ],
        "الجدول الزمني": ["الأشهر 1 - 3", "الأشهر 4 - 6", "الأشهر 7 - 12+"],
    })
  st.table(roadmap_df)

# ==========================================
# TAB 5: ESP32 HARDWARE & RETROFIT BOM
# ==========================================
with tab5:
  st.subheader(t["t5_sub"])
  st.markdown(t["t5_desc"])

  if lang == "English":
    bom_df = pd.DataFrame({
        "Module Component": [
            "Occupancy Detection",
            "HVAC Current Sensing",
            "Indoor Air Quality (IAQ)",
            "AC Relay Control",
            "Smart Bin Fill Level",
            "Smart Irrigation",
        ],
        "Hardware Sensor / Actuator": [
            "PIR Motion Sensor (HC-SR501)",
            "SCT-013-030 Non-Invasive Current Clamp",
            "NDIR CO₂ & Temperature Sensor (MH-Z19)",
            "5V 2-Channel Optical Isolation Relay Module",
            "Ultrasonic Distance Sensor (HC-SR04)",
            "Capacitive Soil Moisture Sensor v1.2",
        ],
        "ESP32 GPIO Pin": [
            "GPIO 14 (Digital IN)",
            "GPIO 35 (ADC Analog IN)",
            "GPIO 34 (ADC Analog IN)",
            "GPIO 26 (Digital OUT)",
            "GPIO 12 (Trig) / GPIO 13 (Echo)",
            "GPIO 32 (ADC Analog IN)",
        ],
        "Function & Retrofit Role": [
            "Detects classroom presence to prevent empty-room AC waste.",
            "Monitors real-time AC compressor power consumption.",
            "Ensures CO₂ levels remain below 1,000 ppm for student alertness.",
            (
                "Automated cutoff relay triggered when rooms remain vacant >5"
                " mins."
            ),
            "Measures waste bin depth to flag collections before overflow.",
            "Optimizes landscape watering based on soil humidity.",
        ],
    })
  else:
    bom_df = pd.DataFrame({
        "مكون الوحدة": [
            "كشف الإشغال والحركة",
            "قياس تيار التكييف",
            "جودة الهواء الداخلي (IAQ)",
            "التحكم في فصل التكييف",
            "قياس امتلاء الحاويات الذكية",
            "الري الذكي للمسطحات",
        ],
        "المستشعر / المشغل الإلكتروني": [
            "مستشعر حركة بالأشعة تحت الحمراء (HC-SR501)",
            "مشبك قياس التيار غير الجراحي (SCT-013-030)",
            "مستشعر ثاني أكسيد الكربون والحرارة (MH-Z19)",
            "وحدة مرحّل عزل بصري قناتين 5 فولت",
            "مستشعر مسافة بالموجات فوق الصوتية (HC-SR04)",
            "مستشعر رطوبة التربة السعوي v1.2",
        ],
        "منفذ ESP32 GPIO": [
            "GPIO 14 (مدخل رقمي)",
            "GPIO 35 (مدخل تناظري ADC)",
            "GPIO 34 (مدخل تناظري ADC)",
            "GPIO 26 (مخرج رقمي)",
            "GPIO 12 (Trig) / GPIO 13 (Echo)",
            "GPIO 32 (مدخل تناظري ADC)",
        ],
        "الوظيفة ودور التحديث": [
            "رصد وجود الطلاب في القاعات لمنع هدر التكييف في الغرف الفارغة.",
            "مراقبة استهلاك ضاغط التكييف للطاقة في الوقت الفعلي.",
            "الحفاظ على مستوى CO₂ أقل من 1,000 جزء في المليون لتركيز الطلاب.",
            "فصل التكييف تلقائياً عند خلو القاعة لأكثر من 5 دقائق.",
            "قياس عمق النفايات لطلب التفريغ قبل امتلاء الحاوية.",
            "تحسين ري الحدائق تلقائياً بناءً على نسبة رطوبة التربة.",
        ],
    })
  st.dataframe(bom_df, use_container_width=True)

# ==========================================
# TAB 6: UN SDGS & UAE NET ZERO 2050
# ==========================================
with tab6:
  st.subheader(t["t6_sub"])

  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(
        f'<div class="info-box">{t["t6_sdg1"]}</div>',
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        f'<div class="info-box">{t["t6_sdg2"]}</div>',
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        f'<div class="info-box">{t["t6_sdg3"]}</div>',
        unsafe_allow_html=True,
    )

  st.markdown("---")
  st.markdown(t["t6_uae_h"])
  st.markdown(
      f'<div class="info-box"><ul>{t["t6_uae_li"]}</ul></div>',
      unsafe_allow_html=True,
  )