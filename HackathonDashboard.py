'''streamlit run HackathonDashboard.py'''

import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import qrcode
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="EcoSmart Campus | Liwa University",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- FOREST GREEN & OFF-WHITE THEME CSS ---
st.markdown(
    """
    <style>
    /* Main Off-White Background */
    .stApp, .main {
        background-color: #F7F9F6;
        color: #1B3B2B;
    }
    
    /* Clean Sidebar */
    [data-testid="stSidebar"] {
        background-color: #143625;
        color: #F7F9F6;
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
        color: #1E3A2F;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #FFFFFF;
        padding: 22px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(20, 54, 37, 0.08);
        border-left: 6px solid #1E5631;
        border-top: 1px solid #DCE5DC;
        border-right: 1px solid #DCE5DC;
        border-bottom: 1px solid #DCE5DC;
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
        background-color: #EDF3ED;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #C8D9C8;
        border-left: 5px solid #2E6F40;
        margin-bottom: 15px;
    }
    .info-box h4 {
        color: #143625 !important;
        margin-top: 0;
    }

    /* Buttons */
    .stButton > button {
        background-color: #1E5631;
        color: #FFFFFF !important;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #143625;
        color: #FFFFFF !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# --- SIDEBAR: INSTITUTIONAL IDENTITY WITH LOGO ---
with st.sidebar:
  # Display Liwa University Logo Image
  try:
    st.image("liwa_logo.png", width=220)
  except Exception:
    st.markdown(
        "<div style='background: white; padding: 10px; border-radius: 8px;"
        " text-align: center; color: #143625 !important; font-weight:"
        " bold;'>[Liwa University Logo]<br><span style='font-size: 11px; color:"
        " #555 !important;'>Save image as 'liwa_logo.png'</span></div>",
        unsafe_allow_html=True,
    )

  st.markdown("---")

  lang = st.selectbox("🌐 Language / اللغة", ["English", "العربية (Arabic)"])

  st.markdown("---")
  st.markdown("### 🏆 Sustainability Hackathon")
  st.markdown("**Project:** EcoSmart Campus")
  st.markdown("**Subtitle:** Next-Gen Resource & Experience Hub")
  st.markdown("---")
  st.markdown(
      "**Project Team:** EcoSmart Innovators <br>(Fathima Faseeha Faizoor &"
      " Shivani Sruthi Soorjith)",
      unsafe_allow_html=True,
  )
  st.markdown(
      "**Supervisor:** Dr. Karamath Ateeq <br>*(Dept. of Engineering &"
      " Computing)*",
      unsafe_allow_html=True,
  )
  st.markdown("**UN SDGs:** 9, 11 & 12")

# --- HEADER TITLE ---
if lang == "English":
  st.title("🌿 EcoSmart Campus : Next-Gen Resource & Experience Hub")
  st.markdown(
      "### Unifying Passive Cooling, Wireless IoT Automation, Indoor Air"
      " Quality & Student Eco-Rewards for Hot-Climate Universities"
  )
else:
  st.title("🌿 كام إيكوسمارت : مركز الموارد والخبرات الذكية")
  st.markdown(
      "### توحيد التبريد السلبي، الأتمتة اللاسلكية، جودة الهواء الداخلي ومكافآت"
      " الطلاب البيئية"
  )

st.markdown("---")

# --- TOP NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Command Center",
    "⚡ Energy3D Thermal & Solar Lab",
    "📱 Student Eco-Rewards & QR Hub",
    "💰 Financial ROI & Scenario Engine",
    "🛠️ ESP32 Hardware & Retrofit BOM",
    "🌍 UN SDGs & UAE Net Zero 2050",
])

# ==========================================
# TAB 1: EXECUTIVE COMMAND CENTER
# ==========================================
with tab1:
  st.subheader("🚀 Campus-Wide Annual Impact & Real-World Scale")

  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.markdown(
        """
            <div class="metric-card">
                <h4>Energy Saved & Generated</h4>
                <h2>568,500 kWh</h2>
                <p><b>Real-Life Scale:</b> ≈ Powering 35 UAE homes for a full year</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        """
            <div class="metric-card">
                <h4>CO₂ Emissions Avoided</h4>
                <h2>227.4 Tons</h2>
                <p><b>Real-Life Scale:</b> ≈ Taking 50 cars off Abu Dhabi roads annually</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        """
            <div class="metric-card">
                <h4>Landscaping Water Saved</h4>
                <h2>8,760 m³</h2>
                <p><b>Real-Life Scale:</b> ≈ Filling 3.5 Olympic swimming pools</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col4:
    st.markdown(
        """
            <div class="metric-card">
                <h4>Landfill Waste Diverted</h4>
                <h2>109.5 Tons</h2>
                <p><b>Real-Life Scale:</b> ≈ 18 full garbage trucks diverted per year</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("### 🏢 Live Zone-by-Zone Campus Telemetry & ESP32 Status")

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
          "Occupied (42 students)",
          "Occupied (85 students)",
          "Vacant (AC Cutoff Active)",
          "Occupied (120 students)",
          "Vacant (Eco-Mode)",
          "Active Generation (375 kWp)",
      ],
      "Indoor Air Quality (CO₂)": [
          "650 ppm (Fresh)",
          "780 ppm (Good)",
          "410 ppm (Fresh)",
          "920 ppm (Acceptable)",
          "500 ppm (Fresh)",
          "N/A (Outdoor)",
      ],
      "HVAC Load (kW)": [
          "12.4 kW",
          "18.2 kW",
          "0.0 kW (Saved)",
          "22.5 kW",
          "8.1 kW",
          "-145 kW (Net Export)",
      ],
      "System Health": [
          "🟢 Online",
          "🟢 Online",
          "🟢 Online",
          "🟢 Online",
          "🟢 Online",
          "☀️ Peak Generating",
      ],
  })
  st.dataframe(zones_df, use_container_width=True)

  st.markdown(
      "### 🔥 Hot-Climate Challenge vs. EcoSmart  Architectural Solution"
  )
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
      "EcoSmart  Upgrades": [
          "Passive glazing reduction to 3×1 m + overhang louvers (−28% peak)",
          "ESP32 PIR motion & CO₂ nodes cut idle AC (21,000 kWh/yr saved)",
          (
              "Soil moisture probes & weather triggers cut water by 30% (56,000"
              " L/day)"
          ),
          "Ultrasonic smart bins + QR rewards triple diversion to 45%",
          "QR-linked smart bins award digital credits for cafeteria perks",
      ],
  })
  st.table(matrix_df)

# ==========================================
# TAB 2: ENERGY3D THERMAL & SOLAR LAB
# ==========================================
with tab2:
  st.subheader(
      "☀️ Abu Dhabi May 2 Hourly Cooling & Solar Load Simulation (Energy3D) "
  )

  hours = np.arange(0, 24)
  baseline_cooling = np.array([
      0.5,
      0.6,
      0.8,
      1.2,
      1.8,
      2.8,
      11.0,
      16.0,
      18.0,
      18.8,
      18.5,
      17.2,
      16.8,
      18.3,
      18.9,
      18.3,
      16.8,
      13.0,
      4.5,
      2.0,
      1.5,
      1.1,
      0.8,
      0.6,
  ])
  optimized_cooling = baseline_cooling * 0.72  # 28% reduction
  solar_generation = (
      np.array([
          0,
          0,
          0,
          0,
          0,
          0.5,
          3.5,
          7.5,
          11.0,
          13.0,
          12.0,
          10.5,
          10.5,
          12.0,
          13.0,
          12.5,
          9.5,
          4.0,
          0.8,
          0,
          0,
          0,
          0,
          0,
      ])
      * 3.75
  )  # Scaled for 375 kWp canopy

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
      title=(
          "24-Hour Energy3D Simulation: Thermal Cooling vs. Solar Generation"
          " (May 2)"
      ),
  )
  fig.update_layout(
      plot_bgcolor="#FFFFFF",
      paper_bgcolor="#F7F9F6",
      font_color="#143625",
      xaxis=dict(gridcolor="#E2E8E2"),
      yaxis=dict(gridcolor="#E2E8E2"),
      legend=dict(
          orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
      ),
  )
  st.plotly_chart(fig, use_container_width=True)

  col1, col2 = st.columns(2)
  with col1:
    st.markdown(
        """
            <div class="info-box">
                <h4>🏛️ Architectural Passive Shading Insights</h4>
                <ul>
                    <li><b>Peak Solar Window:</b> Intense solar radiation hits between 7 AM and 5 PM in Abu Dhabi.</li>
                    <li><b>Glazing Optimization:</b> Reducing window span from 5×3 m to 3×1 m with angled louvers cuts peak cooling demand from <b>18 kW to 13 kW (−28%)</b>.</li>
                    <li><b>Daylight Preservation:</b> Soft ambient daylight (~7,500 kWh/yr saved) is retained without glare.</li>
                </ul>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        """
            <div class="info-box">
                <h4>⚡ Solar Canopy Generation Metrics</h4>
                <ul>
                    <li><b>Capacity:</b> 375 kWp solar canopy spanning 150 parking spaces.</li>
                    <li><b>Annual Yield:</b> Generates 540,000 kWh/yr of clean renewable electricity.</li>
                    <li><b>Microclimate Benefit:</b> Lowers ambient parking temperatures, protecting parked student and faculty vehicles from extreme heat.</li>
                </ul>
            </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# TAB 3: STUDENT ECO-REWARDS & QR HUB
# ==========================================
with tab3:
  st.subheader("📱 Gamified Smart Recycling & QR Eco-Credit Generator")

  col1, col2 = st.columns(2)
  with col1:
    st.markdown("### Generate Student Eco-Reward QR Code")
    student_id = st.text_input("Enter Liwa Student ID", value="LU-2026-9921")
    student_name = st.text_input(
        "Student Name", value="Fathima Faseeha Faizoor"
    )
    bin_location = st.selectbox(
        "Recycling Station",
        [
            "Engineering Building - Smart Bin #1 (PET Plastics)",
            "Library Atrium - Smart Bin #2 (Aluminum Cans)",
            "Student Hub - Smart Bin #3 (Office Paper)",
        ],
    )
    waste_type = st.selectbox(
        "Waste Deposited",
        [
            "PET Bottle (0.5 kg) - 25 Credits",
            "Aluminum Can (0.3 kg) - 35 Credits",
            "Mixed Paper (1.2 kg) - 50 Credits",
        ],
    )

    if st.button("Generate Secure QR Token"):
      qr_payload = f"LiwaEcoSmart:ID={student_id}|Name={student_name}|Bin={bin_location}|Type={waste_type}"
      qr = qrcode.QRCode(version=1, box_size=8, border=2)
      qr.add_data(qr_payload)
      qr.make(fit=True)
      img = qr.make_image(fill_color="#143625", back_color="#F7F9F6")
      buf = io.BytesIO()
      img.save(buf, format="PNG")
      byte_im = buf.getvalue()

      st.image(
          byte_im, width=220, caption="Scan at Liwa Cafeteria Kiosk for Perks!"
      )
      st.success(
          "QR Token Generated! Redeemable for cafeteria coffee & meal"
          " discounts."
      )

  with col2:
    st.markdown("### Live Smart Bin Telemetry & Fill Levels")
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
    st.dataframe(bins_status_df, use_container_width=True)

    st.markdown("### 🍔 Cafeteria Perks & Redemption Catalog")
    st.markdown(
        """
            <div class="info-box">
                <ul>
                    <li><b>☕ 100 Eco-Credits:</b> Free Specialty Coffee at Liwa Campus Café</li>
                    <li><b>🥪 250 Eco-Credits:</b> 20% Discount on Healthy Lunch Meals</li>
                    <li><b>🅿️ 500 Eco-Credits:</b> Reserved Shaded Solar Parking Slot for 1 Month</li>
                    <li><b>📚 1,000 Eco-Credits:</b> Bookstore Voucher for Engineering Textbooks</li>
                </ul>
            </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# TAB 4: FINANCIAL ROI & SCENARIO ENGINE
# ==========================================
with tab4:
  st.subheader("💵 CapEx vs. Utility Payback & 10-Year Scenario Modeling")

  st.markdown(
      "Use the interactive sliders below to model Liwa University's capital"
      " expenditure, electricity tariff rates, and long-term financial returns."
  )

  col_s1, col_s2 = st.columns(2)
  with col_s1:
    capex_input = st.slider(
        "Total CapEx Investment (AED)",
        min_value=100000,
        max_value=500000,
        value=220000,
        step=10000,
    )
  with col_s2:
    tariff_input = st.slider(
        "Electricity Tariff (AED / kWh)",
        min_value=0.30,
        max_value=0.70,
        value=0.45,
        step=0.05,
    )

  annual_kwh = 568500  # Total annual kWh saved + generated
  annual_savings_aed = annual_kwh * tariff_input
  payback_period = capex_input / annual_savings_aed
  net_10yr_savings = (annual_savings_aed * 10) - capex_input

  col_m1, col_m2, col_m3 = st.columns(3)
  with col_m1:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>Annual Utility Savings</h4>
                <h2>AED {annual_savings_aed:,.0f}</h2>
                <p>Based on {annual_kwh:,} kWh annual impact</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_m2:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>Simple Payback Period</h4>
                <h2>{payback_period:.2f} Years</h2>
                <p>Rapid return on green infrastructure</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col_m3:
    st.markdown(
        f"""
            <div class="metric-card">
                <h4>10-Year Net Cumulative Savings</h4>
                <h2>AED {net_10yr_savings:,.0f}</h2>
                <p>Post-CapEx operational net gain</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("### 🗺️ 3-Phase Campus Rollout & Feasibility Roadmap")
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
              "Launch bilingual Arabic/English dashboard & QR-linked smart bins"
              " with campus cafeteria eco-rewards."
          ),
          (
              "Reinvest operational utility savings into 375 kWp parking solar"
              " canopies & AI predictive HVAC scheduling."
          ),
      ],
      "Timeline": ["Months 1 - 3", "Months 4 - 6", "Months 7 - 12+"],
  })
  st.table(roadmap_df)

# ==========================================
# TAB 5: ESP32 HARDWARE & RETROFIT BOM
# ==========================================
with tab5:
  st.subheader("🛠️ Non-Invasive ESP32 Retrofit Architecture & GPIO Pinout BOM")

  st.markdown(
      "EcoSmart is designed for **zero wall rewiring**, utilizing wireless"
      " ESP32 microcontrollers deployed modularly across existing campus"
      " infrastructure."
  )

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
  st.dataframe(bom_df, use_container_width=True)

# ==========================================
# TAB 6: UN SDGS & UAE NET ZERO 2050
# ==========================================
with tab6:
  st.subheader("🌍 Strategic Alignment: UN SDGs & UAE Net Zero 2050")

  col1, col2, col3 = st.columns(3)
  with col1:
    st.markdown(
        """
            <div class="info-box">
                <h4>🎯 UN SDG 9</h4>
                <h3>Industry, Innovation & Infrastructure</h3>
                <p>Deploying non-invasive IoT retrofits, ESP32 microcontrollers, and digital twin analytics across Liwa University with zero structural disruption.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col2:
    st.markdown(
        """
            <div class="info-box">
                <h4>🏙️ UN SDG 11</h4>
                <h3>Sustainable Cities & Communities</h3>
                <p>Optimizing campus resource efficiency, cutting 227.4 tons of annual CO₂ emissions, and fostering an active sustainability culture.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )
  with col3:
    st.markdown(
        """
            <div class="info-box">
                <h4>♻️ UN SDG 12</h4>
                <h3>Responsible Consumption & Production</h3>
                <p>Tripling waste recycling diversion from 15% to 45% via gamified smart bins and reducing landscaping irrigation water use by 30%.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("---")
  st.markdown("### 🇦🇪 Contribution to UAE Net Zero 2050 Strategic Initiative")
  st.markdown(
      """
        <div class="info-box">
            <ul>
                <li><b>Decarbonization of Educational Campuses:</b> Direct reduction of energy consumption through passive window glazing optimization and automated HVAC scheduling.</li>
                <li><b>Renewable Energy Integration:</b> 375 kWp solar canopy installation generating 540,000 kWh/yr of clean solar electricity, directly decreasing reliance on grid fossil fuels.</li>
                <li><b>Water Security in Arid Climates:</b> Smart soil-moisture sensors and weather-linked scheduling save 8,760 m³ of landscaping water annually, supporting UAE water conservation targets.</li>
                <li><b>Bilingual Arabic/English Accessibility:</b> Ensuring seamless deployment and adoption across national and international academic institutions in the UAE.</li>
            </ul>
        </div>
    """,
      unsafe_allow_html=True,
  )

# --- SIDEBAR QR CODE SECTION ---
with st.sidebar:
  st.markdown("---")
  st.markdown("### 📱 Live Web App")
  st.markdown("Scan to open dashboard:")

  # Replace with your deployed GitHub / Streamlit Cloud URL
  dashboard_url = "https://ecosmart-campus-hackathon26.streamlit.app"

  dash_qr = qrcode.QRCode(version=1, box_size=5, border=2)
  dash_qr.add_data(dashboard_url)
  dash_qr.make(fit=True)
  dash_img = dash_qr.make_image(fill_color="#F7F9F6", back_color="#143625")

  buf_dash = io.BytesIO()
  dash_img.save(buf_dash, format="PNG")

  st.image(buf_dash.getvalue(), width=140)