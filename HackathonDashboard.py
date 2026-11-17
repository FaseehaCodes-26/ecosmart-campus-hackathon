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
        font-size: 26px;
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

    /* Decision Engine Live Banner */
    .decision-banner {
        background: linear-gradient(135deg, #143625 0%, #1E5631 100%) !important;
        padding: 22px 26px;
        border-radius: 12px;
        margin: 15px 0 22px 0;
        box-shadow: 0 6px 18px rgba(20, 54, 37, 0.16);
        border-left: 8px solid #F59E0B !important;
    }
    .decision-banner h3, .decision-banner p, .decision-banner span, .decision-banner b {
        color: #FFFFFF !important;
        margin: 0;
    }
    .decision-banner h3 {
        font-size: 22px !important;
        margin-bottom: 8px !important;
    }
    .decision-banner p {
        font-size: 15px !important;
        line-height: 1.5;
        opacity: 0.95;
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

    /* CLEAN TABLES */
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

# --- FULL BILINGUAL DICTIONARY ---
TEXT = {
    "English": {
        "title": "🌿 EcoSmart Campus : Next-Gen Resource & Experience Hub",
        "subtitle": (
            "Unifying Passive Cooling, Smart Timetable + Sensor HVAC Control,"
            " Solar Canopies & Student Eco-Rewards"
        ),
        "header_team": (
            "<strong>Project Team:</strong> Fathima Faseeha Faizoor & Shivani"
            " Sruthi Soorjith | <strong>Supervisor:</strong> Dr. Karamath Ateeq"
            " <em>(Dept. of Engineering & Computing)</em>"
        ),
        "header_sdgs": "<strong>UN SDGs:</strong> 9, 11 & 12",
        "tabs": [
            "📊 Executive Command Center",
            "🧠 Smart Timetable + Sensor + Solar Engine",
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
        "t1_k2_s": "<b>Real-Life Scale:</b> ≈ Taking 50 cars off Abu Dhabi roads annually",
        "t1_k3_t": "Landscaping Water Saved",
        "t1_k3_s": "<b>Real-Life Scale:</b> ≈ Filling 3.5 Olympic swimming pools",
        "t1_k4_t": "Landfill Waste Diverted",
        "t1_k4_s": "<b>Real-Life Scale:</b> ≈ 18 full garbage trucks diverted per year",
        "t1_tel_h": "🏢 Live Zone Telemetry: Timetable Prediction vs. Sensor Reading",
        "t1_toggle": (
            "🎛️ Simulate Students Leaving Engineering Building A (Test Live"
            " ESP32 Relay Cutoff)"
        ),
        "t1_toggle_msg": (
            "⚡ ESP32 PIR Sensor detected 0 occupancy for >15 mins in"
            " Engineering Building A -> Grace period expired -> Relay triggered"
            " ECO MODE / AC CUTOFF (12.4 kW saved instantaneously)!"
        ),
        "csv_btn": "📥 Download Executive Campus Telemetry Report (CSV)",
        "t1_mat_h": "🔥 Hot-Climate Challenge vs. EcoSmart Unified Solution",
        # TAB 2: SMART DECISION ENGINE
        "de_header": "🧠 Unified Timetable + Sensor + Solar HVAC Decision Engine",
        "de_desc": (
            "Connects your class timetable file, live ESP32 occupancy sensors, and"
            " solar canopy output in real time—resolving schedule vs. occupancy"
            " conflicts automatically."
        ),
        "de_sim_title": "🎛️ Interactive Room & Solar Decision Simulator (Test Priority Rules)",
        "de_room_sel": "Select Campus Room / Zone",
        "de_tt_sel": "1. What does the Timetable say?",
        "de_tt_opts": [
            "Class On Now",
            "Class Starting Soon (in 20 mins)",
            "Class Ending Soon (No Next Class)",
            "Room Free (Long Gap)",
        ],
        "de_sens_sel": "2. What does the ESP32 Sensor say?",
        "de_sens_opts": [
            "Occupied (People Detected)",
            "Empty (0 People Detected)",
        ],
        "de_empty_mins": "Minutes Room Has Been Empty",
        "de_solar_sel": "3. Solar Canopy Output Level",
        "de_solar_opts": [
            "High Solar Output (Midday Peak - 375 kWp)",
            "Low Solar Output (Morning / Late Afternoon)",
        ],
        "de_temp_slider": "Outdoor Ambient Temperature (°C)",
        "de_fault_toggle": "⚠️ Simulate Open-Window / Compressor Spike Anomaly",
        "grid_alert_text": (
            "⚠️ EXTREME HEAT ALERT (>45°C): Midday solar pre-cooling boosted"
            " across all scheduled rooms and non-essential EV charging deferred"
            " to protect the Abu Dhabi grid!"
        ),
        "de_kpi1_t": "Timetable Prediction",
        "de_kpi2_t": "Live Sensor Reading",
        "de_kpi3_t": "Active HVAC Mode & Setpoint",
        "de_kpi4_t": "Solar Pre-Cool Timing",
        "de_tt_table_h": "📅 Live University Timetable Feed vs. Sensor Fusion Matrix",
        "de_chart_title": "24-Hour Smart Pre-Cooling Load Curve (Timetable + Sensor + Solar Sync)",
        # TAB 3 (Energy3D)
        "t2_sub": "☀️ Abu Dhabi May 2 Hourly Cooling & Solar Load Simulation (Energy3D)",
        "t2_chart": "24-Hour Energy3D Simulation: Thermal Cooling vs. Solar Generation (May 2)",
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
        # TAB 4 (Rewards)
        "t3_sub": "📱 Gamified Smart Recycling & QR Eco-Credit Generator",
        "t3_c1_h": "### Generate Student Eco-Reward QR Code",
        "t3_id": "Enter Liwa Student ID",
        "t3_name": "Student Name",
        "t3_bin": "Recycling Station",
        "t3_waste": "Waste Deposited",
        "t3_btn": "Generate Secure QR Token",
        "t3_cap": "Scan at Liwa Cafeteria Kiosk for Perks!",
        "t3_ok": "QR Token Generated! Redeemable for cafeteria coffee & meal discounts.",
        "t3_c2_h": "### Live Smart Bin Telemetry & Fill Levels",
        "t3_cat_h": "### 🍔 Cafeteria Perks & Redemption Catalog",
        "t3_cat_li": """
            <li><b>☕ 100 Eco-Credits:</b> Free Specialty Coffee at Liwa Campus Café</li>
            <li><b>🥪 250 Eco-Credits:</b> 20% Discount on Healthy Lunch Meals</li>
            <li><b>🅿️ 500 Eco-Credits:</b> Reserved Shaded Solar Parking Slot for 1 Month</li>
            <li><b>📚 1,000 Eco-Credits:</b> Bookstore Voucher for Engineering Textbooks</li>
        """,
        # TAB 5 (ROI)
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
        # TAB 6 (BOM)
        "t5_sub": "🛠️ Non-Invasive ESP32 Retrofit Architecture & GPIO Pinout BOM",
        "t5_desc": (
            "EcoSmart is designed for **zero wall rewiring**, utilizing wireless"
            " ESP32 microcontrollers deployed modularly across existing campus"
            " infrastructure."
        ),
        # TAB 7 (SDGs)
        "t6_sub": "🌍 Strategic Alignment: UN SDGs & UAE Net Zero 2050",
        "t6_sdg1": (
            "<h4>🎯 UN SDG 9</h4><h3>Industry, Innovation &"
            " Infrastructure</h3><p>Deploying non-invasive IoT retrofits,"
            " ESP32 microcontrollers, and timetable-linked digital analytics"
            " across Liwa University with zero structural disruption.</p>"
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
            <li><b>Decarbonization of Educational Campuses:</b> Direct reduction of energy consumption through passive window glazing optimization and timetable-linked HVAC scheduling.</li>
            <li><b>Renewable Energy Integration:</b> 375 kWp solar canopy installation generating 540,000 kWh/yr of clean renewable electricity, directly syncing midday solar peaks with classroom pre-cooling.</li>
            <li><b>Water Security in Arid Climates:</b> Smart soil-moisture sensors and weather-linked scheduling save 8,760 m³ of landscaping water annually, supporting UAE water conservation targets.</li>
            <li><b>Bilingual Arabic/English Accessibility:</b> Ensuring seamless deployment and adoption across national and international academic institutions in the UAE.</li>
        """,
    },
    "العربية (Arabic)": {
        "title": "🌿 حرم إيكوسمارت الذكي : مركز الموارد والاستدامة المتكامل",
        "subtitle": (
            "دمج التبريد السلبي، التحكم الذكي بالتكييف حسب الجدول الدراسي"
            " والمستشعرات، المظلات الشمسية ومكافآت الطلاب"
        ),
        "header_team": (
            "<strong>فريق العمل:</strong> فاطمة فصيحة فيزور وشيفاني سروثي"
            " سورجيث | <strong>المشرف الأكاديمي:</strong> د. كرامات عتيق"
            " <em>(قسم الهندسة والحوسبة)</em>"
        ),
        "header_sdgs": "<strong>أهداف التنمية المستدامة:</strong> 9، 11 و 12",
        "tabs": [
            "📊 مركز القيادة التنفيذي",
            "🧠 محرك قرارات التكييف (الجدول + المستشعر + الطاقة الشمسية)",
            "⚡ مختبر المحاكاة الحرارية والطاقة الشمسية",
            "📱 مركز مكافآت الطلاب وإعادة التدوير",
            "💰 محرك العائد المالي والجدوى",
            "🛠️ عتاد ESP32 ومخطط التوصيل",
            "🌍 أهداف التنمية المستدامة وحياد الإمارات 2050",
        ],
        # TAB 1 (ARABIC)
        "t1_sub": "🚀 الأثر السنوي الشامل على مستوى الحرم الجامعي والمقياس الواقعي",
        "t1_k1_t": "الطاقة الموفرة والمولدة سنوياً",
        "t1_k1_s": "<b>المقياس الواقعي:</b> ≈ تزويد 35 منزلاً إماراتياً بالكهرباء لمدة عام كامل",
        "t1_k2_t": "انبعاثات ثاني أكسيد الكربون المتجنبة",
        "t1_k2_s": "<b>المقياس الواقعي:</b> ≈ إزالة 50 سيارة من شوارع أبوظبي سنوياً",
        "t1_k3_t": "مياه الري الموفرة سنوياً",
        "t1_k3_s": "<b>المقياس الواقعي:</b> ≈ ملء 3.5 مسابح أولمبية بالكامل",
        "t1_k4_t": "النفايات المحولة عن المكبات",
        "t1_k4_s": "<b>المقياس الواقعي:</b> ≈ تقليل 18 شاحنة نفايات ممتلئة سنوياً",
        "t1_tel_h": "🏢 القياس المباشر للمناطق: توقع الجدول الدراسي مقابل قراءة المستشعر",
        "t1_toggle": (
            "🎛️ محاكاة مغادرة الطلاب لمبنى الهندسة (أ) (اختبار الفصل التلقائي"
            " لمرحل ESP32)"
        ),
        "t1_toggle_msg": (
            "⚡ رصد مستشعر الحركة ESP32 خلو مبنى الهندسة (أ) لأكثر من 15 دقيقة"
            " -> انتهت فترة السماح -> تم التحويل التلقائي للوضع الاقتصادي (توفير"
            " فوري بمقدار 12.4 كيلوواط)!"
        ),
        "csv_btn": "📥 تحميل تقرير القياسات التنفيذي للحرم الجامعي (CSV)",
        "t1_mat_h": "🔥 تحديات المناخ الحار مقابل حلول إيكوسمارت المتكاملة",
        # TAB 2: SMART DECISION ENGINE (ARABIC)
        "de_header": "🧠 محرك قرارات التكييف الذكي (الجدول الدراسي + المستشعرات + الطاقة الشمسية)",
        "de_desc": (
            "يربط ملف الجداول الدراسية للقاعات مع مستشعرات الإشغال ESP32 وإنتاج"
            " المظلات الشمسية لحظياً لحل أي تعارض بين الجدول والواقع الفعلي."
        ),
        "de_sim_title": "🎛️ محاكي القواعد الذكية للقاعات والطاقة الشمسية (اختبر الأولويات)",
        "de_room_sel": "اختر القاعة أو المنطقة الجامعية",
        "de_tt_sel": "1. ماذا يقول الجدول الدراسي؟",
        "de_tt_opts": [
            "توجد محاضرة الآن",
            "محاضرة ستبدأ قريباً (خلال 20 دقيقة)",
            "محاضرة تنتهي قريباً (لا توجد محاضرة بعدها)",
            "القاعة فارغة في الجدول (فترة طويلة)",
        ],
        "de_sens_sel": "2. ماذا يقول مستشعر الحركة ESP32؟",
        "de_sens_opts": [
            "مشغولة (تم رصد طلاب داخل القاعة)",
            "فارغة (لا يوجد أحد داخل القاعة)",
        ],
        "de_empty_mins": "عدد دقائق خلو القاعة حالياً",
        "de_solar_sel": "3. مستوى إنتاج المظلات الشمسية",
        "de_solar_opts": [
            "إنتاج شمسي مرتفع (ذروة الظهيرة - 375 كيلوواط)",
            "إنتاج شمسي منخفض (الصباح الباكر / نهاية اليوم)",
        ],
        "de_temp_slider": "درجة الحرارة الخارجية في أبوظبي (°م)",
        "de_fault_toggle": "⚠️ محاكاة شذوذ استهلاك الطاقة (نافذة مفتوحة / عطل ضاغط)",
        "grid_alert_text": (
            "⚠️ تنبيه حرارة شديدة (>45°م): تم تفعيل التبريد الاستباقي عبر الطاقة"
            " الشمسية وتأجيل شحن المركبات غير الضروري لحماية شبكة أبوظبي!"
        ),
        "de_kpi1_t": "توقع الجدول الدراسي",
        "de_kpi2_t": "قراءة المستشعر الحية",
        "de_kpi3_t": "وضع التكييف ودرجة الحرارة",
        "de_kpi4_t": "توقيت التبريد الشمسي",
        "de_tt_table_h": "📅 مصفوفة مطابقة الجدول الدراسي الحي مع قراءات المستشعرات",
        "de_chart_title": "منحنى التبريد الذكي على مدار 24 ساعة (دمج الجدول + المستشعر + الشمس)",
        # TAB 3 (Energy3D - ARABIC)
        "t2_sub": "☀️ محاكاة أحمال التبريد والطاقة الشمسية في أبوظبي ليوم 2 مايو (Energy3D)",
        "t2_chart": "محاكاة 24 ساعة: التبريد الحراري مقابل توليد الطاقة الشمسية (2 مايو)",
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
        # TAB 4 (Rewards - ARABIC)
        "t3_sub": "📱 نظام إعادة التدوير الذكي ومولد رموز المكافآت الطلابية (QR)",
        "t3_c1_h": "### توليد رمز المكافأة البيئية للطالب (QR)",
        "t3_id": "أدخل الرقم الجامعي للطالب في جامعة ليوا",
        "t3_name": "اسم الطالب",
        "t3_bin": "محطة إعادة التدوير الذكية",
        "t3_waste": "نوع وكمية النفايات المودعة",
        "t3_btn": "توليد رمز QR الآمن للمكافأة",
        "t3_cap": "امسح الرمز في كافتيريا جامعة ليوا للحصول على الخصم!",
        "t3_ok": "تم توليد رمز المكافأة بنجاح! قابل للاستبدال بخصومات القهوة والوجبات.",
        "t3_c2_h": "### القياس المباشر لمستوى امتلاء الحاويات الذكية",
        "t3_cat_h": "### 🍔 كتالوج مكافآت الكافتيريا والحرم الجامعي",
        "t3_cat_li": """
            <li><b>☕ 100 نقطة بيئية:</b> قهوة مختصة مجانية في مقهى حرم جامعة ليوا</li>
            <li><b>🥪 250 نقطة بيئية:</b> خصم 20% على الوجبات الصحية في الكافتيريا</li>
            <li><b>🅿️ 500 نقطة بيئية:</b> موقف سيارة مظلل بالطاقة الشمسية محجوز لمدة شهر</li>
            <li><b>📚 1,000 نقطة بيئية:</b> قسيمة شرائية من مكتبة الجامعة للكتب الهندسية</li>
        """,
        # TAB 5 (ROI - ARABIC)
        "t4_sub": "💵 تحليل النفقات الرأسمالية وفترة الاسترداد والعائد لعشر سنوات",
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
        "impact_badge_title": "🌱 شارة الأثر البيئي الديناميكي (حسب عدد الطلاب)",
        "impact_slider": "مقياس عدد الطلاب النشطين في الحرم",
        "road_h": "### 🗺️ خارطة طريق التنفيذ والجدوى على 3 مراحل",
        # TAB 6 (BOM - ARABIC)
        "t5_sub": "🛠️ معمارية التحديث اللاسلكي ESP32 وجدول توصيل المستشعرات",
        "t5_desc": (
            "تم تصميم نظام إيكوسمارت **دون الحاجة لأي تكسير أو إعادة تمديد"
            " للأسلاك**، باستخدام متحكمات ESP32 اللاسلكية القابلة للتركيب"
            " المباشر."
        ),
        # TAB 7 (SDGs - ARABIC)
        "t6_sub": "🌍 التوافق الاستراتيجي: أهداف التنمية المستدامة ومبادرة الإمارات للحياد المناخي 2050",
        "t6_sdg1": (
            "<h4>🎯 الهدف 9</h4><h3>الصناعة والابتكار والهياكل"
            " الأساسية</h3><p>نشر حلول إنترنت الأشياء اللاسلكية ومتحكمات ESP32"
            " وربطها بالجداول الدراسية في جامعة ليوا دون أي تعطيل للبنية التحتية.</p>"
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
        "t6_uae_h": "### 🇦🇪 المساهمة في المبادرة الاستراتيجية للحياد المناخي 2050 لدولة الإمارات",
        "t6_uae_li": """
            <li><b>إزالة الكربون من المؤسسات التعليمية:</b> خفض مباشر لاستهلاك الطاقة عبر تحسين النوافذ السلبية والجدولة الذكية للتكييف.</li>
            <li><b>دمج الطاقة المتجددة:</b> تركيب مظلات شمسية بقدرة 375 كيلوواط ذروة تنتج 540,000 كيلوواط ساعة/سنة من الكهرباء النظيفة ومزامنتها مع التبريد الاستباقي.</li>
            <li><b>الأمن المائي في المناخات الجافة:</b> مستشعرات رطوبة التربة والجدولة الذكية توفر 8,760 متر مكعب من مياه الري سنوياً.</li>
            <li><b>دعم اللغتين العربية والإنجليزية:</b> ضمان سهولة التطبيق والتبني في كافة الجامعات الوطنية والدولية في دولة الإمارات.</li>
        """,
    },
}

t = TEXT[lang]

# --- CLEAN LOGO DISPLAY ---
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
tab1, tab_de, tab2, tab3, tab4, tab5, tab6 = st.tabs(t["tabs"])

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

    simulate_vacant = st.toggle(t["t1_toggle"], value=False)
    if simulate_vacant:
        st.success(t["t1_toggle_msg"])

    if lang == "English":
        eng_occ = (
            "Empty >15m (Grace Period Expired)"
            if simulate_vacant
            else "Occupied (42 students)"
        )
        eng_hvac = "0.0 kW (Eco-Cutoff)" if simulate_vacant else "12.4 kW (22°C Cool)"
        eng_health = (
            "🟡 Eco-Mode Triggered" if simulate_vacant else "🟢 Cooling Active"
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
            "Timetable Prediction": [
                "Class Scheduled (10:00 - 11:30)",
                "Open Study Hours",
                "Class Starting in 20 mins",
                "Peak Lunch & Club Period",
                "Free Until 2:00 PM",
                "Midday Solar Peak Window",
            ],
            "Live Sensor Reading": [
                eng_occ,
                "Occupied (85 students)",
                "Empty (0 students)",
                "Occupied (120 students)",
                "Empty (0 staff)",
                "375 kWp Generating",
            ],
            "HVAC Load & Setpoint": [
                eng_hvac,
                "18.2 kW (22°C Cool)",
                "6.5 kW (Solar Pre-Cool)",
                "22.5 kW (22°C Cool)",
                "2.1 kW (26°C Eco)",
                "-145 kW (Net Export)",
            ],
            "Decision Engine State": [
                eng_health,
                "🟢 Rule 1: Sensor Override",
                "🔵 Rule 2: Pre-Cooling Early",
                "🟢 Rule 1: Occupied Cool",
                "🟡 Rule 3: Free -> Eco",
                "☀️ Feeding Pre-Cool Load",
            ],
        })
    else:
        eng_occ = (
            "فارغة >15 دقيقة (انتهت مهلة الانتظار)"
            if simulate_vacant
            else "مشغولة (42 طالباً)"
        )
        eng_hvac = "0.0 كيلوواط (مغلق)" if simulate_vacant else "12.4 كيلوواط (تبريد 22°م)"
        eng_health = (
            "🟡 وضع التوفير نشط" if simulate_vacant else "🟢 تبريد نشط"
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
            "توقع الجدول الدراسي": [
                "محاضرة مجدولة (10:00 - 11:30)",
                "ساعات دراسة مفتوحة",
                "محاضرة تبدأ خلال 20 دقيقة",
                "فترة ذروة الأنشطة والاستراحة",
                "فارغ حتى الساعة 2:00 ظهراً",
                "ذروة الإشعاع الشمسي",
            ],
            "قراءة المستشعر الحية": [
                eng_occ,
                "مشغول (85 طالباً)",
                "فارغة (0 طلاب)",
                "مشغول (120 طالباً)",
                "فارغ (0 موظفين)",
                "توليد 375 كيلوواط ذروة",
            ],
            "حمل التكييف ودرجة الحرارة": [
                eng_hvac,
                "18.2 كيلوواط (22°م)",
                "6.5 كيلوواط (تبريد استباقي)",
                "22.5 كيلوواط (22°م)",
                "2.1 كيلوواط (26°م اقتصادي)",
                "-145 كيلوواط (تصدير صافي)",
            ],
            "حالة محرك القرار": [
                eng_health,
                "🟢 قاعدة 1: إشغال فعلي",
                "🔵 قاعدة 2: تبريد مبكر",
                "🟢 قاعدة 1: إشغال فعلي",
                "🟡 قاعدة 3: فارغ -> توفير",
                "☀️ تغذية التبريد الاستباقي",
            ],
        })

    st.dataframe(zones_df, use_container_width=True)

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
                "Schedule vs. Reality Mismatch",
                "Midday Peak Grid Stress",
                "Landscape Watering",
                "Solid Waste & Engagement",
            ],
            "Abu Dhabi Baseline Issue": [
                "70%+ cooling share from unshaded 5×3 m windows",
                "AC runs in empty rooms when classes cancel, or rooms stay hot before class",
                "Cooling peaks at 2 PM while solar canopy peaks at noon",
                "Timer-based irrigation wastes 80,000 L/day",
                "Low recycling diversion (15%) with zero student incentives",
            ],
            "EcoSmart Unified Solution": [
                "Passive glazing reduction to 3×1 m + overhang louvers (−28% peak)",
                "Timetable + Sensor priority rules (15-min grace period + pre-cooling)",
                "Solar-linked pre-cooling shifts cooling into high-solar noon hours",
                "Soil moisture probes & weather triggers cut water by 30% (56,000 L/day)",
                "Ultrasonic smart bins + QR cafeteria rewards triple diversion to 45%",
            ],
        })
    else:
        matrix_df = pd.DataFrame({
            "مجال التحدي": [
                "اكتساب الحرارة الشمسية",
                "التعارض بين الجدول الدراسي والواقع",
                "ذروة الأحمال الكهربائية ظهراً",
                "ري المسطحات الخضراء",
                "النفايات الصلبة وتفاعل الطلاب",
            ],
            "المشكلة الحالية في أبوظبي": [
                "أكثر من 70% من حمل التبريد بسبب النوافذ الكبيرة غير المظللة (5×3 م)",
                "عمل التكييف في قاعات ألغيت محاضراتها أو بقاء القاعة حارة قبل المحاضرة",
                "ذروة التبريد الساعة 2 ظهراً بينما ذروة الطاقة الشمسية عند الظهر",
                "الري المؤقت التقليدي يهدر 80,000 لتر يومياً",
                "انخفاض معدل إعادة التدوير (15% فقط) وغياب الحوافز",
            ],
            "حلول إيكوسمارت المتكاملة": [
                "تقليص النوافذ إلى 3×1 م مع كاسرات شمسية (خفض الذروة بنسبة 28%)",
                "قواعد أولوية تربط الجدول بالمستشعر (مهلة 15 دقيقة + تبريد استباقي)",
                "مزامنة التبريد الاستباقي مع ساعات ذروة إنتاج المظلات الشمسية",
                "مستشعرات رطوبة التربة والطقس تخفض المياه بنسبة 30% (56,000 لتر/يوم)",
                "حاويات ذكية بالموجات فوق الصوتية + مكافآت QR ترفع التدوير إلى 45%",
            ],
        })
    st.table(matrix_df)

# ==========================================
# TAB 2: UNIFIED TIMETABLE + SENSOR + SOLAR ENGINE
# ==========================================
with tab_de:
    st.subheader(t["de_header"])
    st.markdown(t["de_desc"])

    st.markdown(f"#### {t['de_sim_title']}")

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        tt_choice = st.selectbox(t["de_tt_sel"], t["de_tt_opts"])
        peak_temp = st.slider(t["de_temp_slider"], 28, 50, 44)
    with col_ctrl2:
        sens_choice = st.selectbox(t["de_sens_sel"], t["de_sens_opts"])
        empty_mins = st.slider(
            t["de_empty_mins"],
            min_value=0,
            max_value=25,
            value=16 if sens_choice == t["de_sens_opts"][1] else 0,
        )
    with col_ctrl3:
        solar_choice = st.selectbox(t["de_solar_sel"], t["de_solar_opts"])
        inject_fault = st.checkbox(t["de_fault_toggle"], value=False)

    # --- PRIORITY DECISION ENGINE LOGIC ---
    is_occupied = sens_choice == t["de_sens_opts"][0]
    is_high_solar = solar_choice == t["de_solar_opts"][0]
    tt_idx = t["de_tt_opts"].index(tt_choice)

    if lang == "English":
        if is_occupied:
            if tt_idx == 2:
                # Class ending soon & nothing follows -> step up to eco slightly early
                active_mode = "ECO STEP-UP (25°C)"
                solar_timing = "Coast on Stored Cool"
                rule_title = "PRIORITY 1 + EARLY STEP-UP: Room Occupied, Class Ending Soon"
                rule_desc = (
                    "Sensor confirms students are present, so comfort is maintained, but"
                    " because the timetable shows no class following this one, the"
                    " compressor steps up to 25°C Eco-Coast 10 minutes before dismissal."
                )
                relay_badge = "🟢 ON (Eco-Coast)"
            else:
                active_mode = "ACTIVE COOLING (22°C)"
                solar_timing = "Standard Comfort Hold"
                rule_title = "PRIORITY 1 OVERRIDE: Sensor Detects People -> Keep Cooling"
                rule_desc = (
                    "ESP32 PIR & CO₂ sensors detect active occupancy. Regardless of what"
                    " the timetable says (even during unscheduled study sessions), the"
                    " room stays in 22°C Active Cooling mode."
                )
                relay_badge = "🟢 ON (Full Cool)"
        else:
            # Sensor sees nobody
            if tt_idx == 1:
                # Class starting soon (15-30 mins)
                active_mode = "PRE-COOLING (21°C)"
                if is_high_solar:
                    solar_timing = "Start 30 Mins Early (High Solar)"
                    rule_title = "PRIORITY 2 + SOLAR BOOST: Early Solar Pre-Cooling Active"
                    rule_desc = (
                        "Room is currently empty, but timetable shows a class starting soon."
                        " Because Solar Canopy output is HIGH, pre-cooling starts 30 minutes"
                        " early using free midday solar power to bank thermal comfort."
                    )
                else:
                    solar_timing = "Start 15 Mins Early (Low Solar)"
                    rule_title = "PRIORITY 2 + SOLAR SAVE: Delayed Pre-Cooling Active"
                    rule_desc = (
                        "Room is empty and a class starts soon. Because Solar Canopy output is"
                        " LOW, pre-cooling waits until 15 minutes before class—just enough to"
                        " reach 22°C on arrival without wasting grid power."
                    )
                relay_badge = "🔵 ON (Pre-Cool)"
            elif tt_idx == 0:
                # Class on now, but sensor sees nobody
                if empty_mins < 15:
                    active_mode = f"GRACE HOLD ({15 - empty_mins}m left)"
                    solar_timing = "Standby Hold"
                    rule_title = f"PRIORITY 4 GRACE PERIOD: Waiting for Late Arrivals ({empty_mins}/15 mins)"
                    rule_desc = (
                        "Timetable says a class is on now, but sensor sees nobody. Holding"
                        " temperature during the 15-minute grace period in case students or"
                        " faculty are running late."
                    )
                    relay_badge = "🟠 HOLD (Grace Timer)"
                else:
                    active_mode = "ECO / OFF (26°C)"
                    solar_timing = "Power Diverted to Other Zones"
                    rule_title = "PRIORITY 4 TRIGGERED: Grace Period Expired -> Class Treated as Cancelled"
                    rule_desc = (
                        f"Room remained empty for {empty_mins} mins (>15 min grace period)"
                        " despite scheduled class. System classifies session as cancelled/moved"
                        " and switches AC to 26°C Eco / OFF."
                    )
                    relay_badge = "🟡 ECO / OFF (Saved)"
            else:
                # Class ending soon (empty) or Room free
                active_mode = "ECO / OFF (26°C)"
                solar_timing = "Zero Wasted Load"
                rule_title = "PRIORITY 3: Empty Room + No Upcoming Class -> Eco Mode / OFF"
                rule_desc = (
                    "Both the timetable and ESP32 sensor confirm no occupancy is present or"
                    " expected soon. AC is switched to 26°C Eco / OFF immediately."
                )
                relay_badge = "🟡 ECO / OFF (Saved)"
    else:
        if is_occupied:
            if tt_idx == 2:
                active_mode = "توفير تدريجي (25°م)"
                solar_timing = "استغلال البرودة المخزنة"
                rule_title = "الأولوية 1 + إنهاء مبكر: القاعة مشغولة والمحاضرة تنتهي قريباً"
                rule_desc = (
                    "المستشعر يؤكد وجود الطلاب، ولأن الجدول يوضح عدم وجود محاضرة تالية،"
                    " يرفع النظام درجة الحرارة تدريجياً إلى 25°م قبل نهاية المحاضرة بـ 10 دقائق."
                )
                relay_badge = "🟢 يعمل (توفير تدريجي)"
            else:
                active_mode = "تبريد نشط (22°م)"
                solar_timing = "تثبيت الراحة الحرارية"
                rule_title = "الأولوية 1 (تجاوز الجدول): المستشعر يرصد طلاباً -> استمرار التبريد"
                rule_desc = (
                    "مستشعرات الحركة وثاني أكسيد الكربون ترصد وجود طلاب داخل القاعة."
                    " يتم الإبقاء على التبريد النشط (22°م) بغض النظر عن الجدول الدراسي."
                )
                relay_badge = "🟢 يعمل (تبريد كامل)"
        else:
            if tt_idx == 1:
                active_mode = "تبريد استباقي (21°م)"
                if is_high_solar:
                    solar_timing = "بدء مبكر بـ 30 دقيقة (شمس قوية)"
                    rule_title = "الأولوية 2 + تعزيز شمسي: تبريد استباقي مبكر عبر الطاقة الشمسية"
                    rule_desc = (
                        "القاعة فارغة حالياً ولكن ستبدأ محاضرة قريباً. نظراً لارتفاع إنتاج"
                        " المظلات الشمسية، يبدأ التبريد قبل 30 دقيقة لتخزين البرودة مجاناً."
                    )
                else:
                    solar_timing = "بدء متأخر بـ 15 دقيقة (شمس منخفضة)"
                    rule_title = "الأولوية 2 + توفير الشبكة: تأخير التبريد الاستباقي"
                    rule_desc = (
                        "القاعة فارغة وستبدأ محاضرة قريباً. نظراً لانخفاض الإنتاج الشمسي،"
                        " يتأخر التبريد ليبدأ قبل 15 دقيقة فقط لتجنب استهلاك كهرباء الشبكة."
                    )
                relay_badge = "🔵 يعمل (تبريد استباقي)"
            elif tt_idx == 0:
                if empty_mins < 15:
                    active_mode = f"فترة سماح ({15 - empty_mins} د متبقية)"
                    solar_timing = "انتظار مؤقت"
                    rule_title = f"الأولوية 4 (فترة السماح): انتظار وصول الطلاب ({empty_mins}/15 دقيقة)"
                    rule_desc = (
                        "الجدول يوضح وجود محاضرة الآن ولكن القاعة فارغة. يتم الانتظار لمدة"
                        " 15 دقيقة تحسباً لتأخر الطلاب أو المحاضر قبل فصل التكييف."
                    )
                    relay_badge = "🟠 انتظار (مؤقت السماح)"
                else:
                    active_mode = "وضع اقتصادي / إيقاف (26°م)"
                    solar_timing = "توجيه الطاقة لقاعات أخرى"
                    rule_title = "الأولوية 4 (إلغاء تلقائي): انتهت مهلة الـ 15 دقيقة -> القاعة ملغاة"
                    rule_desc = (
                        f"بقيت القاعة فارغة لمدة {empty_mins} دقيقة رغم وجود محاضرة في الجدول."
                        " يعتبر النظام المحاضرة ملغاة ويحول التكييف فوراً إلى 26°م / إيقاف."
                    )
                    relay_badge = "🟡 توفير / إيقاف"
            else:
                active_mode = "وضع اقتصادي / إيقاف (26°م)"
                solar_timing = "صفر هدر للطاقة"
                rule_title = "الأولوية 3: قاعة فارغة ولا توجد محاضرات -> وضع اقتصادي / إيقاف"
                rule_desc = (
                    "الجدول الدراسي والمستشعر يؤكدان عدم وجود طلاب حالياً أو قريباً."
                    " يتم تحويل التكييف فوراً إلى الوضع الاقتصادي 26°م أو الإيقاف."
                )
                relay_badge = "🟡 توفير / إيقاف"

    # DISPLAY LIVE DECISION ENGINE BANNER
    st.markdown(
        f"""
        <div class="decision-banner">
            <h3>⚡ {rule_title}</h3>
            <p>{rule_desc}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if peak_temp > 45:
        st.markdown(
            f'<div class="grid-alert">{t["grid_alert_text"]}</div>',
            unsafe_allow_html=True,
        )

    # 4 KPI CARDS FOR DECISION OUTPUT
    dk1, dk2, dk3, dk4 = st.columns(4)
    with dk1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>{t['de_kpi1_t']}</h4>
                <h2>{tt_choice.split('(')[0].strip()}</h2>
                <p>Timetable File Input</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with dk2:
        sens_sub = (
            f"Empty for {empty_mins} mins"
            if not is_occupied
            else "PIR + CO₂ Active"
        )
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>{t['de_kpi2_t']}</h4>
                <h2>{sens_choice.split('(')[0].strip()}</h2>
                <p>{sens_sub}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with dk3:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>{t['de_kpi3_t']}</h4>
                <h2>{active_mode}</h2>
                <p>{relay_badge}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with dk4:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>{t['de_kpi4_t']}</h4>
                <h2>{solar_timing}</h2>
                <p>{solar_choice.split('(')[0].strip()}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # LIVE TIMETABLE + SENSOR FUSION TABLE ACROSS CAMPUS ROOMS
    st.markdown(f"#### {t['de_tt_table_h']}")
    if lang == "English":
        fusion_df = pd.DataFrame({
            "Room ID": ["ENG-101 (Selected)", "ENG-104", "LAB-202", "BUS-305", "AUD-01"],
            "Timetable File Schedule": [
                tt_choice,
                "11:00 - 12:30 (In Progress)",
                "11:30 - 13:00 (Starts in 20m)",
                "10:00 - 11:00 (Ending Soon)",
                "Free Until 15:00",
            ],
            "ESP32 Sensor Reading": [
                f"{sens_choice.split('(')[0].strip()} ({empty_mins}m empty)" if not is_occupied else "Occupied (38 students)",
                "Empty for 18 mins",
                "Empty (0 students)",
                "Occupied (29 students)",
                "Occupied (15 club members)",
            ],
            "Solar Canopy Sync": [
                solar_choice.split("(")[0].strip(),
                "High Solar (375 kWp)",
                "High Solar -> Early Pre-Cool",
                "Midday Solar Coast",
                "High Solar -> Offset Load",
            ],
            "Final Decision Rule Action": [
                f"{active_mode} ({relay_badge})",
                "Grace Expired (>15m) -> Class Cancelled -> 26°C Eco",
                "Pre-Cool 30m Early using Midday Solar Peak",
                "Step up to 25°C Eco 10m before class ends",
                "Sensor Override -> Keep 22°C Cooling Active",
            ],
        })
    else:
        fusion_df = pd.DataFrame({
            "رمز القاعة": ["ENG-101 (المحددة)", "ENG-104", "LAB-202", "BUS-305", "AUD-01"],
            "جدول القاعات الدراسي": [
                tt_choice,
                "11:00 - 12:30 (جارية حالياً)",
                "11:30 - 13:00 (تبدأ خلال 20 د)",
                "10:00 - 11:00 (تنتهي قريباً)",
                "فارغة حتى الساعة 15:00",
            ],
            "قراءة مستشعر ESP32": [
                f"{sens_choice.split('(')[0].strip()} ({empty_mins} د)" if not is_occupied else "مشغولة (38 طالباً)",
                "فارغة منذ 18 دقيقة",
                "فارغة (0 طلاب)",
                "مشغولة (29 طالباً)",
                "مشغولة (15 طالباً لنشاط طلابي)",
            ],
            "مزامنة المظلات الشمسية": [
                solar_choice.split("(")[0].strip(),
                "إنتاج شمسي مرتفع",
                "شمس مرتفعة -> تبريد مبكر",
                "استغلال برودة الظهيرة",
                "تغطية الحمل بالطاقة الشمسية",
            ],
            "القرار النهائي للمحرك": [
                f"{active_mode} ({relay_badge})",
                "انتهت مهلة 15 د -> محاضرة ملغاة -> توفير 26°م",
                "تبريد استباقي قبل 30 د عبر ذروة الشمس",
                "رفع الحرارة إلى 25°م قبل نهاية المحاضرة بـ 10 د",
                "تجاوز الجدول لوجود طلاب -> تبريد نشط 22°م",
            ],
        })

    st.dataframe(fusion_df, use_container_width=True)

    # 24-HOUR CURVE SHOWING TIMETABLE + SOLAR PRE-COOLING SHIFT
    @st.cache_resource
    def train_load_model():
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
        X_train = pd.DataFrame({"hour": hours_data, "temp": temp_data, "occ": occ_data})
        rf_model = RandomForestRegressor(n_estimators=60, random_state=42)
        rf_model.fit(X_train, cooling_kw)
        return rf_model

    rf_model = train_load_model()
    hours_24 = np.arange(0, 24)
    hourly_temps = peak_temp - 9 * np.cos((hours_24 - 14) * np.pi / 12)
    hourly_occ = np.where((hours_24 >= 8) & (hours_24 <= 18), 75, 8)

    X_pred = pd.DataFrame({"hour": hours_24, "temp": hourly_temps, "occ": hourly_occ})
    unoptimized_kw = rf_model.predict(X_pred)

    # Smart Rule Optimized Curve: shifts cooling into high solar midday (10am-1pm) and cuts empty rooms
    smart_rule_kw = unoptimized_kw * 0.78
    smart_rule_kw[10:13] *= 1.18  # Midday solar pre-cooling boost
    smart_rule_kw[14:17] *= 0.74  # Reduced afternoon peak draw due to pre-cooled thermal mass
    smart_rule_kw[19:] *= 0.40    # Empty evening eco cutoff

    if inject_fault:
        unoptimized_kw[11:16] *= 1.42

    df_plot = pd.DataFrame({
        "Hour": hours_24,
        "Static Timer HVAC (kW)": unoptimized_kw,
        "Timetable + Sensor + Solar Rule HVAC (kW)": smart_rule_kw,
    })

    fig_de = px.area(
        df_plot,
        x="Hour",
        y=[
            "Static Timer HVAC (kW)",
            "Timetable + Sensor + Solar Rule HVAC (kW)",
        ],
        color_discrete_sequence=["#B45309", "#1E5631"],
        title=t["de_chart_title"],
    )
    fig_de.update_layout(
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
    st.plotly_chart(fig_de, use_container_width=True)

# ==========================================
# TAB 3: ENERGY3D THERMAL & SOLAR LAB
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
# TAB 4: STUDENT ECO-REWARDS & QR HUB
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
# TAB 5: FINANCIAL ROI & SCENARIO ENGINE
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
                "Wireless IoT Sensor + Timetable Pilot",
                "Bilingual UI & Smart Bins",
                "Solar Canopies & Full Campus Pre-Cooling",
            ],
            "Key Actions": [
                (
                    "Deploy wireless ESP32 occupancy/IAQ nodes linked to room"
                    " timetables & soil moisture sensors in 1 building."
                ),
                (
                    "Launch bilingual Arabic/English dashboard & QR-linked smart"
                    " bins with campus cafeteria eco-rewards."
                ),
                (
                    "Reinvest operational utility savings into 375 kWp parking"
                    " solar canopies synced with midday pre-cooling."
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
                "ربط المستشعرات اللاسلكية بالجدول الدراسي",
                "الواجهة ثنائية اللغة والحاويات الذكية",
                "المظلات الشمسية والتبريد الاستباقي الشامل",
            ],
            "الإجراءات الرئيسية": [
                "نشر عقد ESP32 اللاسلكية وربطها بملف الجداول الدراسية ومستشعرات رطوبة التربة في مبنى واحد.",
                "إطلاق لوحة التحكم بالعربية والإنجليزية وربط الحاويات الذكية بمكافآت الكافتيريا.",
                "إعادة استثمار الوفورات المالية في تركيب مظلات شمسية 375 كيلوواط ومزامنتها مع التبريد الاستباقي.",
            ],
            "الجدول الزمني": ["الأشهر 1 - 3", "الأشهر 4 - 6", "الأشهر 7 - 12+"],
        })
    st.table(roadmap_df)

# ==========================================
# TAB 6: ESP32 HARDWARE & RETROFIT BOM
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
                "AC Mode & Relay Control",
                "Smart Bin Fill Level",
                "Smart Irrigation",
            ],
            "Hardware Sensor / Actuator": [
                "PIR Motion Sensor (HC-SR501)",
                "SCT-013-030 Non-Invasive Current Clamp",
                "NDIR CO₂ & Temperature Sensor (MH-Z19)",
                "5V 2-Channel Optical Isolation Relay + IR Blaster",
                "Ultrasonic Distance Sensor (HC-SR04)",
                "Capacitive Soil Moisture Sensor v1.2",
            ],
            "ESP32 GPIO Pin": [
                "GPIO 14 (Digital IN)",
                "GPIO 35 (ADC Analog IN)",
                "GPIO 34 (ADC Analog IN)",
                "GPIO 26 (Relay) / GPIO 27 (IR)",
                "GPIO 12 (Trig) / GPIO 13 (Echo)",
                "GPIO 32 (ADC Analog IN)",
            ],
            "Function & Timetable Fusion Role": [
                "Overrides timetable if students are present; starts 15m grace timer if empty.",
                "Monitors real-time AC compressor power consumption.",
                "Ensures CO₂ levels remain below 1,000 ppm for student alertness.",
                "Switches AC between 21°C Pre-Cool, 22°C Cool, and 26°C Eco / OFF.",
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
                "التحكم في وضع ودرجة التكييف",
                "قياس امتلاء الحاويات الذكية",
                "الري الذكي للمسطحات",
            ],
            "المستشعر / المشغل الإلكتروني": [
                "مستشعر حركة بالأشعة تحت الحمراء (HC-SR501)",
                "مشبك قياس التيار غير الجراحي (SCT-013-030)",
                "مستشعر ثاني أكسيد الكربون والحرارة (MH-Z19)",
                "وحدة مرحّل 5 فولت + مرسل أشعة تحت حمراء (IR)",
                "مستشعر مسافة بالموجات فوق الصوتية (HC-SR04)",
                "مستشعر رطوبة التربة السعوي v1.2",
            ],
            "منفذ ESP32 GPIO": [
                "GPIO 14 (مدخل رقمي)",
                "GPIO 35 (مدخل تناظري ADC)",
                "GPIO 34 (مدخل تناظري ADC)",
                "GPIO 26 (Relay) / GPIO 27 (IR)",
                "GPIO 12 (Trig) / GPIO 13 (Echo)",
                "GPIO 32 (مدخل تناظري ADC)",
            ],
            "الوظيفة ودور الدمج مع الجدول": [
                "يتجاوز الجدول عند وجود طلاب؛ ويشغل مؤقت السماح (15 د) عند خلو القاعة.",
                "مراقبة استهلاك ضاغط التكييف للطاقة في الوقت الفعلي.",
                "الحفاظ على مستوى CO₂ أقل من 1,000 جزء في المليون لتركيز الطلاب.",
                "تبديل التكييف بين التبريد الاستباقي (21°م) والتبريد (22°م) والتوفير (26°م).",
                "قياس عمق النفايات لطلب التفريغ قبل امتلاء الحاوية.",
                "تحسين ري الحدائق تلقائياً بناءً على نسبة رطوبة التربة.",
            ],
        })
    st.dataframe(bom_df, use_container_width=True)

# ==========================================
# TAB 7: UN SDGS & UAE NET ZERO 2050
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