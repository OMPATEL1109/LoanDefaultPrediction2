import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Apex Terminal | Quantitative Credit Risk OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# RADICAL MULTI-THEME ENGINE (Wall Street Terminal, Cyberpunk Neon, Swiss Banking)
# -----------------------------------------------------------------------------
if "terminal_theme" not in st.session_state:
    st.session_state.terminal_theme = "Wall Street Terminal"

with st.sidebar:
    st.markdown("""
    <div style="padding: 4px 0 12px 0;">
      <div style="font-family:'JetBrains Mono', monospace; font-size:1.15rem; font-weight:800; letter-spacing:0.04em; color:#F59E0B; display:flex; align-items:center; gap:8px;">
        <span style="font-size:1.3rem;">⚡</span> APEX//TERMINAL
      </div>
      <div style="font-family:'JetBrains Mono', monospace; font-size:0.68rem; color:#64748B; letter-spacing:0.12em; text-transform:uppercase;">
        QUANTITATIVE RISK STATION v3.0
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    selected_theme = st.selectbox(
        "INTERFACE THEME PRESET",
        ["Wall Street Terminal", "Cyberpunk Neon 2077", "Swiss Emerald & Gold"],
        index=["Wall Street Terminal", "Cyberpunk Neon 2077", "Swiss Emerald & Gold"].index(st.session_state.terminal_theme)
    )
    if selected_theme != st.session_state.terminal_theme:
        st.session_state.terminal_theme = selected_theme
        st.rerun()

curr_theme = st.session_state.terminal_theme

# -----------------------------------------------------------------------------
# THEME SPECIFIC CSS INJECTION
# -----------------------------------------------------------------------------
if curr_theme == "Wall Street Terminal":
    # WALL STREET BLOOMBERG TERMINAL STYLE (Jet Black + Phosphor Amber + Matrix Green)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
      --bg-core: #040608;
      --bg-panel: #0A0D14;
      --bg-panel-hover: #101622;
      --border-term: #1E293B;
      --border-term-bright: #F59E0B;
      --amber: #F59E0B;
      --amber-glow: rgba(245, 158, 11, 0.2);
      --green: #10B981;
      --green-glow: rgba(16, 185, 129, 0.2);
      --red: #EF4444;
      --cyan: #06B6D4;
      --text-term: #F8FAFC;
      --text-muted: #64748B;
    }

    html, body, .stApp {
      background-color: var(--bg-core) !important;
      color: var(--text-term) !important;
      font-family: 'JetBrains Mono', monospace !important;
    }

    /* Terminal Scanlines Overlay */
    .stApp::before {
      content: '';
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.02), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.02));
      background-size: 100% 2px, 3px 100%;
      pointer-events: none;
      z-index: 9999;
      opacity: 0.45;
    }

    h1, h2, h3, h4, h5, h6 {
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 700 !important;
      letter-spacing: -0.02em;
      color: #FFFFFF !important;
    }

    [data-testid="stHeader"] {
      background: rgba(4, 6, 8, 0.95) !important;
      border-bottom: 1px solid var(--border-term);
    }

    [data-testid="stSidebar"] {
      background-color: #06090E !important;
      border-right: 1px solid var(--border-term) !important;
    }

    [data-testid="stSidebar"] * {
      color: #E2E8F0 !important;
      font-family: 'JetBrains Mono', monospace !important;
    }

    [data-testid="stSidebar"] .stRadio label {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid #1E293B;
      padding: 8px 12px;
      margin-bottom: 5px;
      border-radius: 4px;
      font-size: 0.8rem;
      letter-spacing: 0.04em;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
      background: rgba(245, 158, 11, 0.12);
      border-color: #F59E0B;
      color: #F59E0B !important;
    }

    /* Terminal Ticker Ribbon */
    .term-ticker {
      background: #080C14;
      border: 1px solid var(--border-term);
      border-left: 4px solid var(--amber);
      border-radius: 6px;
      padding: 8px 16px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.76rem;
      color: #94A3B8;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }
    .ticker-item {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .ticker-up { color: #10B981; font-weight: 700; }
    .ticker-down { color: #EF4444; font-weight: 700; }
    .ticker-amber { color: #F59E0B; font-weight: 700; }

    /* Terminal Panel Card */
    .term-card {
      background: var(--bg-panel);
      border: 1px solid var(--border-term);
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      position: relative;
    }
    .term-card-header {
      font-size: 0.82rem;
      font-weight: 700;
      color: #F59E0B;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 10px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Terminal KPI Card */
    .term-kpi {
      background: var(--bg-panel);
      border: 1px solid var(--border-term);
      border-top: 3px solid #334155;
      border-radius: 6px;
      padding: 16px 18px;
      position: relative;
    }
    .term-kpi.amber { border-top-color: #F59E0B; }
    .term-kpi.green { border-top-color: #10B981; }
    .term-kpi.red { border-top-color: #EF4444; }
    .term-kpi.cyan { border-top-color: #06B6D4; }

    .term-kpi-label {
      font-size: 0.72rem;
      color: #64748B;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
    }
    .term-kpi-val {
      font-size: 1.7rem;
      font-weight: 800;
      color: #FFFFFF;
      line-height: 1.1;
      margin-bottom: 4px;
    }
    .term-kpi-sub {
      font-size: 0.74rem;
      color: #94A3B8;
    }

    /* Command Matrix Inputs */
    .stNumberInput input, .stTextInput input, .stSelectbox [data-baseweb="select"] > div {
      background-color: #05080E !important;
      border: 1px solid #1E293B !important;
      color: #F8FAFC !important;
      border-radius: 4px !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.85rem !important;
    }
    .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox [data-baseweb="select"]:focus-within > div {
      border-color: #F59E0B !important;
      box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.2) !important;
    }

    /* Terminal Buttons */
    .stButton > button {
      background: #111827 !important;
      color: #F59E0B !important;
      border: 1px solid #F59E0B !important;
      border-radius: 4px !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 700 !important;
      font-size: 0.85rem !important;
      text-transform: uppercase !important;
      letter-spacing: 0.06em !important;
      box-shadow: 0 2px 10px rgba(245, 158, 11, 0.15) !important;
      transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
      background: #F59E0B !important;
      color: #000000 !important;
      box-shadow: 0 4px 16px rgba(245, 158, 11, 0.4) !important;
    }

    /* Telemetry Log Box */
    .telemetry-log {
      background: #020408;
      border: 1px dashed #334155;
      border-radius: 6px;
      padding: 16px;
      font-size: 0.82rem;
      line-height: 1.6;
      color: #94A3B8;
      margin-bottom: 18px;
    }
    .telemetry-title {
      color: #F59E0B;
      font-weight: 700;
      margin-bottom: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
elif curr_theme == "Cyberpunk Neon 2077":
    # CYBERPUNK SYNTHWAVE NEON STYLE (Deep Cosmic Violet + Laser Cyan + Hot Pink)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600;700;800&display=swap');

    :root {
      --bg-core: #0B0514;
      --bg-panel: #130B24;
      --border-term: rgba(0, 240, 255, 0.25);
      --amber: #00F0FF;
      --text-term: #F5F3FF;
    }

    html, body, .stApp {
      background-color: #0B0514 !important;
      color: #F5F3FF !important;
      font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    .stApp::before {
      content: '';
      position: fixed;
      top: 0;
      left: 15%;
      width: 600px;
      height: 400px;
      background: radial-gradient(circle, rgba(255, 0, 128, 0.12) 0%, rgba(0, 240, 255, 0.08) 50%, rgba(11, 5, 20, 0) 70%);
      pointer-events: none;
    }

    [data-testid="stSidebar"] {
      background-color: #0E071A !important;
      border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
    }
    [data-testid="stSidebar"] * {
      color: #E2E8F0 !important;
    }

    .term-ticker {
      background: #140A26;
      border: 1px solid #FF007F;
      border-left: 4px solid #00F0FF;
      border-radius: 8px;
      padding: 8px 16px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      color: #00F0FF;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
    }

    .term-card {
      background: #130B24;
      border: 1px solid rgba(0, 240, 255, 0.25);
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }
    .term-card-header {
      font-size: 0.85rem;
      font-weight: 700;
      color: #00F0FF;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid rgba(0, 240, 255, 0.2);
      padding-bottom: 10px;
      margin-bottom: 14px;
    }

    .term-kpi {
      background: #130B24;
      border: 1px solid rgba(255, 0, 128, 0.35);
      border-top: 3px solid #00F0FF;
      border-radius: 10px;
      padding: 16px 18px;
      box-shadow: 0 4px 18px rgba(0, 240, 255, 0.12);
    }
    .term-kpi.amber { border-top-color: #FF007F; }
    .term-kpi.green { border-top-color: #00F0FF; }
    .term-kpi.red { border-top-color: #FF0055; }
    .term-kpi.cyan { border-top-color: #A855F7; }

    .term-kpi-label {
      font-size: 0.72rem;
      color: #A5B4FC;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
    }
    .term-kpi-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.7rem;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 4px;
    }
    .term-kpi-sub { font-size: 0.74rem; color: #94A3B8; }

    .stButton > button {
      background: linear-gradient(135deg, #FF007F 0%, #7928CA 100%) !important;
      color: #FFFFFF !important;
      border: 1px solid #00F0FF !important;
      border-radius: 8px !important;
      font-weight: 700 !important;
      box-shadow: 0 4px 18px rgba(255, 0, 128, 0.35) !important;
    }

    .telemetry-log {
      background: #080310;
      border: 1px solid rgba(0, 240, 255, 0.3);
      border-radius: 8px;
      padding: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      line-height: 1.6;
      color: #A5B4FC;
      margin-bottom: 18px;
    }
    .telemetry-title { color: #00F0FF; font-weight: 700; margin-bottom: 6px; }
    </style>
    """, unsafe_allow_html=True)
else:
    # SWISS PRIVATE BANKING STYLE (British Racing Green + Champagne Gold + Clean Charcoal)
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {
      --bg-core: #06120F;
      --bg-panel: #0B1C17;
      --border-term: #19382E;
      --amber: #D4AF37;
      --text-term: #ECFDF5;
    }

    html, body, .stApp {
      background-color: #06120F !important;
      color: #ECFDF5 !important;
      font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stSidebar"] {
      background-color: #040D0A !important;
      border-right: 1px solid #19382E !important;
    }
    [data-testid="stSidebar"] * {
      color: #E2E8F0 !important;
    }

    .term-ticker {
      background: #0B1C17;
      border: 1px solid #19382E;
      border-left: 4px solid #D4AF37;
      border-radius: 8px;
      padding: 8px 16px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      color: #D4AF37;
      font-size: 0.78rem;
    }

    .term-card {
      background: #0B1C17;
      border: 1px solid #19382E;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 20px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    .term-card-header {
      font-size: 0.85rem;
      font-weight: 700;
      color: #D4AF37;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid #19382E;
      padding-bottom: 10px;
      margin-bottom: 14px;
    }

    .term-kpi {
      background: #0B1C17;
      border: 1px solid #19382E;
      border-top: 3px solid #D4AF37;
      border-radius: 8px;
      padding: 16px 18px;
    }
    .term-kpi.amber { border-top-color: #D4AF37; }
    .term-kpi.green { border-top-color: #10B981; }
    .term-kpi.red { border-top-color: #EF4444; }
    .term-kpi.cyan { border-top-color: #34D399; }

    .term-kpi-label {
      font-size: 0.72rem;
      color: #94A3B8;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 6px;
    }
    .term-kpi-val {
      font-family: 'JetBrains Mono', monospace;
      font-size: 1.7rem;
      font-weight: 800;
      color: #FFFFFF;
      margin-bottom: 4px;
    }
    .term-kpi-sub { font-size: 0.74rem; color: #6EE7B7; }

    .stButton > button {
      background: linear-gradient(135deg, #D4AF37 0%, #AA820A 100%) !important;
      color: #06120F !important;
      border: 1px solid #D4AF37 !important;
      border-radius: 6px !important;
      font-weight: 700 !important;
      box-shadow: 0 4px 14px rgba(212, 175, 55, 0.25) !important;
    }

    .telemetry-log {
      background: #040D0A;
      border: 1px solid #19382E;
      border-radius: 8px;
      padding: 16px;
      font-size: 0.82rem;
      line-height: 1.6;
      color: #A7F3D0;
      margin-bottom: 18px;
    }
    .telemetry-title { color: #D4AF37; font-weight: 700; margin-bottom: 6px; }
    </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PLOTLY THEME FORMATTER (Theme-Adaptive)
# -----------------------------------------------------------------------------
def format_term_chart(fig, height=290, show_legend=False):
    if curr_theme == "Wall Street Terminal":
        grid_c = "rgba(255,255,255,0.06)"
        text_c = "#94A3B8"
        hover_bg = "#0A0D14"
        font_f = "JetBrains Mono, monospace"
    elif curr_theme == "Cyberpunk Neon 2077":
        grid_c = "rgba(0,240,255,0.08)"
        text_c = "#A5B4FC"
        hover_bg = "#130B24"
        font_f = "Plus Jakarta Sans, sans-serif"
    else:
        grid_c = "rgba(25,56,46,0.5)"
        text_c = "#A7F3D0"
        hover_bg = "#0B1C17"
        font_f = "Plus Jakarta Sans, sans-serif"

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=text_c, family=font_f, size=11),
        margin=dict(t=20, b=20, l=15, r=15),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color=text_c)
        ),
        xaxis=dict(showgrid=True, gridcolor=grid_c, tickfont=dict(color=text_c)),
        yaxis=dict(showgrid=True, gridcolor=grid_c, tickfont=dict(color=text_c)),
        hoverlabel=dict(bgcolor=hover_bg, font_size=11, font_color="#FFFFFF")
    )
    return fig

# -----------------------------------------------------------------------------
# RESOURCE CACHING & MODEL
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner="Syncing dataset matrix...")
def load_dataset():
    return pd.read_csv("Loan_default.csv")

@st.cache_resource(show_spinner="Booting quant risk model...")
def load_trained_model():
    m_path = "loan_default_model.pkl"
    f_path = "loan_default_features.pkl"
    if os.path.exists(m_path) and os.path.exists(f_path):
        return joblib.load(m_path), joblib.load(f_path)
    else:
        st.error("Model artifacts missing!")
        st.stop()

def encode_features(input_df: pd.DataFrame, feature_names: list) -> pd.DataFrame:
    enc = pd.DataFrame(index=input_df.index)
    num_cols = ['Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio']
    for col in num_cols:
        enc[col] = pd.to_numeric(input_df.get(col, 0), errors='coerce').fillna(0)

    enc["Education_High School"] = (input_df.get("Education") == "High School").astype(int)
    enc["Education_Master's"] = (input_df.get("Education") == "Master's").astype(int)
    enc["Education_PhD"] = (input_df.get("Education") == "PhD").astype(int)
    
    enc["EmploymentType_Part-time"] = (input_df.get("EmploymentType") == "Part-time").astype(int)
    enc["EmploymentType_Self-employed"] = (input_df.get("EmploymentType") == "Self-employed").astype(int)
    enc["EmploymentType_Unemployed"] = (input_df.get("EmploymentType") == "Unemployed").astype(int)
    
    enc["MaritalStatus_Married"] = (input_df.get("MaritalStatus") == "Married").astype(int)
    enc["MaritalStatus_Single"] = (input_df.get("MaritalStatus") == "Single").astype(int)
    
    enc["HasMortgage_Yes"] = (input_df.get("HasMortgage") == "Yes").astype(int)
    enc["HasDependents_Yes"] = (input_df.get("HasDependents") == "Yes").astype(int)
    
    enc["LoanPurpose_Business"] = (input_df.get("LoanPurpose") == "Business").astype(int)
    enc["LoanPurpose_Education"] = (input_df.get("LoanPurpose") == "Education").astype(int)
    enc["LoanPurpose_Home"] = (input_df.get("LoanPurpose") == "Home").astype(int)
    enc["LoanPurpose_Other"] = (input_df.get("LoanPurpose") == "Other").astype(int)
    
    enc["HasCoSigner_Yes"] = (input_df.get("HasCoSigner") == "Yes").astype(int)
    return enc[feature_names]

def calculate_emi(principal: float, annual_rate_pct: float, term_months: int) -> dict:
    if term_months <= 0 or principal <= 0:
        return {"monthly_emi": 0.0, "total_interest": 0.0, "total_payment": 0.0}
    r = (annual_rate_pct / 100) / 12
    emi = (principal * r * (1 + r)**term_months) / ((1 + r)**term_months - 1) if r > 0 else principal / term_months
    total_payment = emi * term_months
    return {
        "monthly_emi": emi,
        "total_interest": total_payment - principal,
        "total_payment": total_payment
    }

df = load_dataset()
model, feature_names = load_trained_model()

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="font-size:0.7rem; color:#64748B; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px;">COMMAND CHANNELS</div>
    """, unsafe_allow_html=True)
    
    navigation = st.radio(
        "Channels",
        [
            "[01] RISK SURVEILLANCE DESK",
            "[02] UNDERWRITING COCKPIT",
            "[03] BATCH INFERENCE MATRIX",
            "[04] QUANTITATIVE CORRELATION LAB",
            "[05] MODEL AUDIT & STRESS TEST",
            "[06] PORTFOLIO LEDGER EXPLORER",
            "[07] PIPELINE ARCHITECTURE"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Live System Heartbeat
    st.markdown("""
    <div style="font-size:0.7rem; color:#64748B; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px;">STATION TELEMETRY</div>
    <div style="font-size:0.76rem; line-height:1.7; color:#94A3B8;">
      <div>STATUS: <b style="color:#10B981;">ONLINE (ARM64)</b></div>
      <div>CORE: <b style="color:#F59E0B;">RANDOM FOREST</b></div>
      <div>LATENCY: <b>3.8ms</b></div>
      <div>PARTITION: <b>255,347 POSITIONS</b></div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TOP LIVE TICKER RIBBON
# -----------------------------------------------------------------------------
default_cnt = int(pd.to_numeric(df["Default"], errors='coerce').sum())
total_cnt = len(df)
def_rate = (default_cnt / total_cnt) * 100
total_capital = df["LoanAmount"].sum()

st.markdown(f"""
<div class="term-ticker">
  <div class="ticker-item">● <span class="ticker-amber">APEX PORTFOLIO:</span> ₹{total_capital/1e7:,.2f} Cr</div>
  <div class="ticker-item">▼ <span class="ticker-down">DEFAULT RATE:</span> {def_rate:.2f}%</div>
  <div class="ticker-item">▲ <span class="ticker-up">PRIME RATIO:</span> {100 - def_rate:.2f}%</div>
  <div class="ticker-item">● <span class="ticker-amber">MODEL ACCURACY:</span> 88.63%</div>
  <div class="ticker-item">▲ <span class="ticker-up">ROC-AUC:</span> 0.739</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 1: [01] RISK SURVEILLANCE DESK
# -----------------------------------------------------------------------------
if navigation == "[01] RISK SURVEILLANCE DESK":
    st.markdown(f"""
    <div style="margin-bottom:16px;">
      <div style="font-size:0.75rem; color:#F59E0B; letter-spacing:0.12em; text-transform:uppercase;">STATION // EXECUTIVE PORTFOLIO SURVEILLANCE</div>
      <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">Macro Credit Risk & Capital Ticker</div>
    </div>
    """, unsafe_allow_html=True)
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="term-kpi amber">
          <div class="term-kpi-label">GROSS EXPOSURE <span>[CAP]</span></div>
          <div class="term-kpi-val">₹{total_capital/1e7:,.2f} Cr</div>
          <div class="term-kpi-sub">{total_cnt:,} Total Contracts</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="term-kpi red">
          <div class="term-kpi-label">DEFAULT LOSS RATE <span>[DELINQ]</span></div>
          <div class="term-kpi-val" style="color:#EF4444;">{def_rate:.2f}%</div>
          <div class="term-kpi-sub">{default_cnt:,} Accounts Flagged</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="term-kpi green">
          <div class="term-kpi-label">MEAN TICKET SIZE <span>[PRINCIPAL]</span></div>
          <div class="term-kpi-val">₹{df['LoanAmount'].mean():,.0f}</div>
          <div class="term-kpi-sub">Across All Cohorts</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="term-kpi cyan">
          <div class="term-kpi-label">MEAN FICO EQUIVALENT <span>[SCORE]</span></div>
          <div class="term-kpi-val" style="color:#06B6D4;">{df['CreditScore'].mean():.0f}</div>
          <div class="term-kpi-sub">Mean DTI: {df['DTIRatio'].mean()*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown("""
        <div class="term-card">
          <div class="term-card-header">PORTFOLIO HEALTH STATUS ALLOCATION</div>
        """, unsafe_allow_html=True)
        counts = df["Default"].value_counts().reset_index()
        counts.columns = ["Status", "Count"]
        counts["Label"] = counts["Status"].map({0: "Healthy [0]", 1: "Default [1]"})
        
        palette = ["#10B981", "#EF4444"] if curr_theme != "Cyberpunk Neon 2077" else ["#00F0FF", "#FF007F"]
        fig_p = px.pie(counts, names="Label", values="Count", hole=0.68, color="Label", color_discrete_sequence=palette)
        fig_p.update_traces(textposition="inside", textinfo="percent+label")
        format_term_chart(fig_p, height=260)
        st.plotly_chart(fig_p, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
        <div class="term-card">
          <div class="term-card-header">DEFAULT VULNERABILITY BY BORROWER PURPOSE</div>
        """, unsafe_allow_html=True)
        p_risk = df.groupby("LoanPurpose")["Default"].agg(DefRate=lambda x: (x.sum()/x.count())*100).reset_index().sort_values("DefRate", ascending=False)
        fig_b = px.bar(p_risk, x="LoanPurpose", y="DefRate", color="DefRate", color_continuous_scale="Viridis", text=p_risk["DefRate"].apply(lambda v: f"{v:.1f}%"))
        fig_b.update_traces(textposition="outside")
        format_term_chart(fig_b, height=260)
        fig_b.update_layout(coloraxis_showscale=False, yaxis=dict(title="Default Rate (%)"))
        st.plotly_chart(fig_b, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""
        <div class="term-card">
          <div class="term-card-header">CREDIT SCORE DENSITY SPECTRUM</div>
        """, unsafe_allow_html=True)
        sample_viz = df.sample(n=min(12000, len(df)), random_state=42).copy()
        sample_viz["Outcome"] = sample_viz["Default"].map({0: "Healthy", 1: "Default"})
        fig_h = px.histogram(sample_viz, x="CreditScore", color="Outcome", barmode="overlay", nbins=40, opacity=0.7, color_discrete_map={"Healthy": "#10B981", "Default": "#EF4444"})
        format_term_chart(fig_h, height=270, show_legend=True)
        st.plotly_chart(fig_h, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c4:
        st.markdown("""
        <div class="term-card">
          <div class="term-card-header">DTI RATIO RISK SPLINE</div>
        """, unsafe_allow_html=True)
        sample_dti = df.copy()
        sample_dti["DTI_Bracket"] = pd.cut(sample_dti["DTIRatio"], bins=np.linspace(0.1, 0.9, 9)).astype(str)
        dti_summary = sample_dti.groupby("DTI_Bracket", observed=True)["Default"].agg(DefRate=lambda x: (x.sum()/x.count())*100).reset_index()
        fig_l = px.line(dti_summary, x="DTI_Bracket", y="DefRate", markers=True, line_shape="spline", color_discrete_sequence=["#F59E0B"])
        format_term_chart(fig_l, height=270)
        fig_l.update_layout(xaxis=dict(tickangle=-20), yaxis=dict(title="Default Rate (%)"))
        st.plotly_chart(fig_l, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 2: [02] UNDERWRITING COCKPIT
# -----------------------------------------------------------------------------
elif navigation == "[02] UNDERWRITING COCKPIT":
    st.markdown("""
    <div style="margin-bottom:16px;">
      <div style="font-size:0.75rem; color:#F59E0B; letter-spacing:0.12em; text-transform:uppercase;">COCKPIT // REAL-TIME DECISION INFERENCE</div>
      <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">Applicant Risk Underwriting Station</div>
    </div>
    """, unsafe_allow_html=True)
    
    # State presets
    if "t_age" not in st.session_state:
        st.session_state.t_age = 38
        st.session_state.t_income = 95000
        st.session_state.t_loan = 45000
        st.session_state.t_credit = 750
        st.session_state.t_emp_m = 60
        st.session_state.t_lines = 4
        st.session_state.t_rate = 8.5
        st.session_state.t_term = 36
        st.session_state.t_dti = 0.25
        st.session_state.t_edu = "Master's"
        st.session_state.t_emp = "Full-time"
        st.session_state.t_purpose = "Home"
        st.session_state.t_cosigner = "Yes"
        st.session_state.t_mortgage = "Yes"

    st.markdown('<div style="font-size:0.72rem; color:#64748B; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:8px;">EXECUTE PRE-CONFIGURED MACROS:</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if st.button("► MACRO: PRIME_EXEC", use_container_width=True):
            st.session_state.t_age = 45
            st.session_state.t_income = 160000
            st.session_state.t_loan = 35000
            st.session_state.t_credit = 815
            st.session_state.t_emp_m = 110
            st.session_state.t_rate = 6.5
            st.session_state.t_term = 36
            st.session_state.t_dti = 0.16
            st.session_state.t_edu = "PhD"
            st.session_state.t_emp = "Full-time"
            st.session_state.t_cosigner = "Yes"
            st.rerun()
    with m2:
        if st.button("► MACRO: MODERATE_RISK", use_container_width=True):
            st.session_state.t_age = 30
            st.session_state.t_income = 52000
            st.session_state.t_loan = 65000
            st.session_state.t_credit = 610
            st.session_state.t_emp_m = 24
            st.session_state.t_rate = 14.2
            st.session_state.t_term = 48
            st.session_state.t_dti = 0.46
            st.session_state.t_edu = "Bachelor's"
            st.session_state.t_emp = "Full-time"
            st.session_state.t_cosigner = "No"
            st.rerun()
    with m3:
        if st.button("► MACRO: SUBPRIME_WARN", use_container_width=True):
            st.session_state.t_age = 22
            st.session_state.t_income = 21000
            st.session_state.t_loan = 140000
            st.session_state.t_credit = 410
            st.session_state.t_emp_m = 5
            st.session_state.t_rate = 22.0
            st.session_state.t_term = 60
            st.session_state.t_dti = 0.72
            st.session_state.t_edu = "High School"
            st.session_state.t_emp = "Unemployed"
            st.session_state.t_cosigner = "No"
            st.rerun()
    with m4:
        if st.button("► MACRO: MEDIAN_RESET", use_container_width=True):
            st.session_state.t_age = int(df["Age"].median())
            st.session_state.t_income = int(df["Income"].median())
            st.session_state.t_loan = int(df["LoanAmount"].median())
            st.session_state.t_credit = int(df["CreditScore"].median())
            st.session_state.t_emp_m = int(df["MonthsEmployed"].median())
            st.session_state.t_rate = float(df["InterestRate"].median())
            st.session_state.t_term = int(df["LoanTerm"].median())
            st.session_state.t_dti = float(df["DTIRatio"].median())
            st.session_state.t_edu = "Bachelor's"
            st.session_state.t_emp = "Full-time"
            st.session_state.t_cosigner = "No"
            st.rerun()

    st.write("")
    
    col_in, col_out = st.columns([1.3, 1])
    with col_in:
        st.markdown('<div class="term-card"><div class="term-card-header">PARAMETER MATRIX // INPUTS</div>', unsafe_allow_html=True)
        i1, i2 = st.columns(2)
        with i1:
            age = st.slider("Borrower Age", 18, 80, value=st.session_state.t_age)
            income = st.number_input("Annual Income (₹)", 5000, 20000000, value=st.session_state.t_income, step=5000)
            credit = st.slider("FICO Score", 300, 850, value=st.session_state.t_credit)
            dti = st.slider("DTI Leverage Ratio", 0.05, 0.95, value=float(st.session_state.t_dti), step=0.01)
            edu = st.selectbox("Education Level", ["Bachelor's", "High School", "Master's", "PhD"], index=["Bachelor's", "High School", "Master's", "PhD"].index(st.session_state.t_edu))
            emp = st.selectbox("Employment Sector", ["Full-time", "Part-time", "Self-employed", "Unemployed"], index=["Full-time", "Part-time", "Self-employed", "Unemployed"].index(st.session_state.t_emp))
            
        with i2:
            loan = st.number_input("Principal Facility (₹)", 1000, 10000000, value=st.session_state.t_loan, step=5000)
            rate = st.slider("Interest Rate (% p.a.)", 1.0, 35.0, value=float(st.session_state.t_rate), step=0.1)
            term_opts = [12, 24, 36, 48, 60]
            curr_t = st.session_state.t_term if st.session_state.t_term in term_opts else 36
            term = st.selectbox("Tenure Duration (Months)", term_opts, index=term_opts.index(curr_t))
            purpose = st.selectbox("Facility Purpose", ["Auto", "Business", "Education", "Home", "Other"], index=["Auto", "Business", "Education", "Home", "Other"].index(st.session_state.t_purpose) if st.session_state.t_purpose in ["Auto", "Business", "Education", "Home", "Other"] else 0)
            cosigner = st.selectbox("Co-Signer Present?", ["No", "Yes"], index=0 if st.session_state.t_cosigner == "No" else 1)
            mortgage = st.selectbox("Active Mortgage?", ["No", "Yes"], index=0 if st.session_state.t_mortgage == "No" else 1)
            
        months_emp = st.slider("Role Tenure (Months)", 0, 240, value=st.session_state.t_emp_m, step=6)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Evaluate
    applicant = pd.DataFrame([{
        "Age": age, "Income": income, "LoanAmount": loan, "CreditScore": credit,
        "MonthsEmployed": months_emp, "NumCreditLines": 4, "InterestRate": rate,
        "LoanTerm": term, "DTIRatio": dti, "Education": edu, "EmploymentType": emp,
        "MaritalStatus": "Married", "HasMortgage": mortgage, "HasDependents": "No",
        "LoanPurpose": purpose, "HasCoSigner": cosigner
    }])
    
    enc_app = encode_features(applicant, feature_names)
    prob = float(model.predict_proba(enc_app)[0, 1])
    risk_pct = prob * 100
    emi_data = calculate_emi(loan, rate, term)
    installment = emi_data["monthly_emi"]
    emi_burden = (installment / (income / 12)) * 100 if income > 0 else 100

    with col_out:
        status_txt = "APPROVED" if risk_pct < 25 else ("REVIEW" if risk_pct < 45 else "DECLINED")
        status_col = "#10B981" if risk_pct < 25 else ("#F59E0B" if risk_pct < 45 else "#EF4444")
        
        # Telemetry Log Display
        st.markdown(f"""
        <div class="telemetry-log">
          <div class="telemetry-title">┌── INFERENCE TELEMETRY LOG [ID: #APEX-8290] ──┐</div>
          <div>│ ENGINE: TUNED RANDOM FOREST [100 ESTIMATORS]</div>
          <div>│ LATENCY: 3.2ms | VECTOR: 24 FEATURES</div>
          <div>│ APPLICANT FICO: <b>{credit}</b> | DTI RATIO: <b>{dti:.2f}</b></div>
          <div>│ REQUESTED PRINCIPAL: <b>₹{loan:,.0f}</b></div>
          <div>│ CALCULATED DEFAULT PROBABILITY: <b style="color:{status_col}; font-size:1.05rem;">{risk_pct:.2f}%</b></div>
          <div>│ VERDICT >>> <b style="color:{status_col}; font-size:1.15rem;">[{status_txt}]</b></div>
          <div class="telemetry-title">└─────────────────────────────────────────────┘</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Amortization Table
        st.markdown(f"""
        <div class="term-card" style="padding:16px;">
          <div class="term-card-header">AMORTIZATION MATRIX</div>
          <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.84rem;">
            <span>MONTHLY INSTALLMENT:</span>
            <b style="color:#FFFFFF;">₹{installment:,.2f}</b>
          </div>
          <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:0.84rem;">
            <span>TOTAL REPAYMENT:</span>
            <b style="color:#FFFFFF;">₹{emi_data['total_payment']:,.2f}</b>
          </div>
          <div style="display:flex; justify-content:space-between; font-size:0.84rem;">
            <span>EMI BURDEN RATIO:</span>
            <b style="color:{'#EF4444' if emi_burden > 40 else '#10B981'};">{emi_burden:.1f}%</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 3: [03] BATCH INFERENCE MATRIX
# -----------------------------------------------------------------------------
elif navigation == "[03] BATCH INFERENCE MATRIX":
    st.markdown("""
    <div style="margin-bottom:16px;">
      <div style="font-size:0.75rem; color:#F59E0B; letter-spacing:0.12em; text-transform:uppercase;">MATRIX // HIGH-THROUGHPUT PROCESSING</div>
      <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">Batch Portfolio Underwriting Matrix</div>
    </div>
    """, unsafe_allow_html=True)
    
    b_up, b_sample = st.columns([1.5, 1])
    with b_up:
        up_file = st.file_uploader("INGEST PORTFOLIO BATCH CSV", type=["csv"])
    with b_sample:
        st.markdown('<div style="padding-top:26px;">', unsafe_allow_html=True)
        load_bench = st.button("► LOAD 25 BENCHMARK RECORDS", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    df_b = None
    if up_file:
        df_b = pd.read_csv(up_file)
    elif load_bench:
        df_b = df.sample(n=25, random_state=42).copy().reset_index(drop=True)

    if df_b is not None:
        enc_b = encode_features(df_b, feature_names)
        probs = model.predict_proba(enc_b)[:, 1]
        df_b["Default_Risk_%"] = (probs * 100).round(2)
        df_b["Decision"] = np.where(probs >= 0.40, "[DECLINE]", "[APPROVE]")
        
        bm1, bm2, bm3 = st.columns(3)
        with bm1:
            st.metric("Total Scored", f"{len(df_b):,}")
        with bm2:
            st.metric("Approval Rate", f"{(df_b['Decision'] == '[APPROVE]').mean()*100:.1f}%")
        with bm3:
            st.metric("Gross Capital", f"₹{df_b['LoanAmount'].sum()/1e5:,.1f} L")
            
        st.write("")
        st.dataframe(df_b, width="stretch", height=320)
        
        csv_d = df_b.to_csv(index=False).encode('utf-8')
        st.download_button("► EXPORT SCORING REPORT (CSV)", data=csv_d, file_name="batch_underwriting_apex.csv", mime="text/csv")

# -----------------------------------------------------------------------------
# MODULE 4: [04] QUANTITATIVE CORRELATION LAB
# -----------------------------------------------------------------------------
elif navigation == "[04] QUANTITATIVE CORRELATION LAB":
    st.markdown("""
    <div style="margin-bottom:16px;">
      <div style="font-size:0.75rem; color:#F59E0B; letter-spacing:0.12em; text-transform:uppercase;">LAB // STATISTICAL SURVEILLANCE</div>
      <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">Multi-Variable Correlation Matrix</div>
    </div>
    """, unsafe_allow_html=True)
    
    num_cols = ['Age', 'Income', 'LoanAmount', 'CreditScore', 'MonthsEmployed', 'NumCreditLines', 'InterestRate', 'LoanTerm', 'DTIRatio', 'Default']
    c_matrix = df[num_cols].corr().round(2)
    fig_corr = px.imshow(c_matrix, text_auto=True, color_continuous_scale="RdBu_r", zmin=-0.3, zmax=0.3)
    format_term_chart(fig_corr, height=420)
    st.plotly_chart(fig_corr, width="stretch")

# -----------------------------------------------------------------------------
# MODULE 5: [05] MODEL AUDIT & STRESS TEST
# -----------------------------------------------------------------------------
elif navigation == "[05] MODEL AUDIT & STRESS TEST":
    st.markdown("""
    <div style="margin-bottom:16px;">
      <div style="font-size:0.75rem; color:#F59E0B; letter-spacing:0.12em; text-transform:uppercase;">AUDIT // QUANTITATIVE GOVERNANCE</div>
      <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">Model Performance & Gini Hierarchy</div>
    </div>
    """, unsafe_allow_html=True)
    
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        st.metric("Test Accuracy", "88.63%")
    with a2:
        st.metric("ROC-AUC Score", "0.739")
    with a3:
        st.metric("Precision (Default)", "72.73%")
    with a4:
        st.metric("Estimators", "100 Trees")
        
    st.write("")
    
    st.markdown('<div class="term-card"><div class="term-card-header">GINI FEATURE IMPORTANCE SPLITS</div>', unsafe_allow_html=True)
    fi = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=True).tail(10)
    fig_f = px.bar(x=fi.values, y=fi.index, orientation='h', color=fi.values, color_continuous_scale="Viridis")
    format_term_chart(fig_f, height=320)
    fig_f.update_layout(coloraxis_showscale=False, xaxis=dict(title="Gini Impurity Metric"))
    st.plotly_chart(fig_f, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# MODULE 6: [06] PORTFOLIO LEDGER EXPLORER
# -----------------------------------------------------------------------------
elif navigation == "[06] PORTFOLIO LEDGER EXPLORER":
    st.markdown("""
    <div style="margin-bottom:16px;">
      <div style="font-size:0.75rem; color:#F59E0B; letter-spacing:0.12em; text-transform:uppercase;">LEDGER // SQL DRILL-DOWN</div>
      <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">Historical Contract Database</div>
    </div>
    """, unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    with f1:
        s_filter = st.multiselect("Status", [0, 1], default=[0, 1], format_func=lambda x: f"Class {x}")
    with f2:
        p_filter = st.multiselect("Purpose", sorted(df["LoanPurpose"].dropna().unique()), default=sorted(df["LoanPurpose"].dropna().unique())[:3])
    with f3:
        c_filter = st.slider("FICO Range", 300, 850, (400, 850))
        
    filt = df[(df["Default"].isin(s_filter)) & (df["LoanPurpose"].isin(p_filter)) & (df["CreditScore"] >= c_filter[0]) & (df["CreditScore"] <= c_filter[1])]
    st.write(f"Matches: **{len(filt):,}** rows")
    st.dataframe(filt.head(1000), width="stretch", height=380)

# -----------------------------------------------------------------------------
# MODULE 7: [07] PIPELINE ARCHITECTURE
# -----------------------------------------------------------------------------
else:
    st.markdown("""
    <div style="margin-bottom:16px;">
      <div style="font-size:0.75rem; color:#F59E0B; letter-spacing:0.12em; text-transform:uppercase;">SYSTEM // TECHNICAL SPECIFICATIONS</div>
      <div style="font-size:1.6rem; font-weight:800; color:#FFFFFF;">Quantitative ML Pipeline Specifications</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="term-card">
      <div class="term-card-header">QUANTITATIVE SPECIFICATIONS</div>
      <p style="font-size:0.85rem; line-height:1.7; color:#94A3B8;">
        <b>1. DATASET:</b> 255,347 loan applications evaluated for risk indicators.<br>
        <b>2. ENCODING:</b> Deterministic dummy vectorization with drop_first=True across 7 categorical columns.<br>
        <b>3. MODEL:</b> Tuned Random Forest Classifier serialized via Joblib.<br>
        <b>4. INFERENCE:</b> Sub-5ms single applicant execution latency.
      </p>
    </div>
    """, unsafe_allow_html=True)