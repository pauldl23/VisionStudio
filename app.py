import streamlit as st
import pandas as pd
from ml_engine import EyeHealthModel
import time
import random

# --- SETUP ---
st.set_page_config(
    page_title="VisionStudio | Clinical Intelligence",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load Engine
@st.cache_resource
def get_engine():
    return EyeHealthModel()

engine = get_engine()
# Self-healing cache bypass if an old version is stuck in memory
if not hasattr(engine, 'generate_patients'):
    st.cache_resource.clear()
    engine = get_engine()

# --- STATE MANAGEMENT ---
def init_state():
    defaults = {
        'current_page': "Diagnostics",
        'sleep_val': 7.5,
        'lux_val': 450,
        'vitamin_val': 900,
        'screen_time': 6.8,
        'manual_override': False,
        'active_models': 14,
        'accuracy': 92.4,
        'model_version': "v2.4.0",
        'patients_df': engine.generate_patients()
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# --- CALLBACKS ---
def nav_to(page):
    st.session_state.current_page = page

def reset_analysis():
    st.session_state.sleep_val = 7.5
    st.session_state.lux_val = 450
    st.session_state.vitamin_val = 900
    st.session_state.screen_time = 6.8

def retrain_model():
    st.session_state.accuracy += random.choice([-0.5, 0.5])
    # split "v2.4.X" and increment X
    parts = st.session_state.model_version.split('.')
    new_patch = int(parts[2]) + 1
    st.session_state.model_version = f"{parts[0]}.{parts[1]}.{new_patch}"

# Calculate dependent metrics based on state
health_score = engine.predict(
    st.session_state.sleep_val, 
    st.session_state.vitamin_val,
    st.session_state.screen_time,
    st.session_state.lux_val
)
status, color, message = engine.get_insights(health_score)
drift, tear = engine.get_realtime_metrics(st.session_state.lux_val, st.session_state.sleep_val)

# Dynamic AI Status
ai_status_text = "Processing Neural Node 7"
pulse_class = "animate-pulse"
if st.session_state.manual_override:
    ai_status_text = "User Controlled Mode"
    pulse_class = ""

# --- SIDEBAR NAV ---
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0;">
        <h2 style="color: #4edea3; font-weight: 800; letter-spacing: -1px; margin-bottom: 0;">VISIONSTUDIO</h2>
        <p style="color: #4edea3; font-size: 10px; font-family: monospace; opacity: 0.6;">v2.4.0-Alpha</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### CLINICAL INTELLIGENCE")
    
    # Custom CSS to highlight active button
    st.markdown(f"""
    <style>
        div[data-testid="stSidebar"] button p {{ color: #bbcabf; }}
        div[data-testid="stSidebar"] button:contains("{st.session_state.current_page}") {{
            background-color: rgba(78, 222, 163, 0.1) !important;
            border-right: 2px solid #4edea3 !important;
        }}
        div[data-testid="stSidebar"] button:contains("{st.session_state.current_page}") p {{
            color: #4edea3 !important;
            font-weight: 700 !important;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.button("👁️ Diagnostics", use_container_width=True, on_click=nav_to, args=("Diagnostics",))
    st.button("👥 Patient Flow", use_container_width=True, on_click=nav_to, args=("Patient Flow",))
    st.button("🧠 Model Insights", use_container_width=True, on_click=nav_to, args=("Model Insights",))
    st.button("🔍 Explorer", use_container_width=True, on_click=nav_to, args=("Explorer",))
    st.button("📊 Lab Reports", use_container_width=True, on_click=nav_to, args=("Lab Reports",))
    
    st.divider()
    st.markdown("### SYSTEM")
    st.button("🖥️ System Status", use_container_width=True, on_click=nav_to, args=("System Status",))
    st.button("⚙️ Preferences", use_container_width=True, on_click=nav_to, args=("Preferences",))

# --- MAIN HEADER ---
csv_data = st.session_state.patients_df.to_csv(index=False).encode('utf-8')

col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.markdown(f"""
        <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">Diagnostic Intelligence Dashboard</h1>
        <p style="color: #bbcabf; display: flex; align-items: center; gap: 8px;">
            <span class="{pulse_class}" style="display: inline-block; width: 8px; height: 8px; background: #4edea3; border-radius: 50%; box-shadow: 0 0 10px #4edea3;"></span>
            Live AI Inference Status: {ai_status_text}
        </p>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        search_term = st.text_input("🔍 Search diagnostics...", label_visibility="collapsed")
    with c2:
        st.download_button(
            label="💾 Export Dataset",
            data=csv_data,
            file_name='vision_studio_patient_flow.csv',
            mime='text/csv',
            use_container_width=True
        )
    with c3:
        st.button("➕ New Analysis", on_click=reset_analysis, type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== ROUTING =====
if st.session_state.current_page == "Diagnostics":
    # --- TIER 1: KPI GRID ---
    col1, col2, col3, col4 = st.columns(4)

    def kpi_card(title, value, unit, trend, icon="trending_up"):
        st.markdown(f"""
        <div class="glass-panel" style="padding: 20px; border-radius: 16px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <p style="font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #bbcabf;">{title}</p>
                <span style="color: #4edea3; font-size: 12px; font-weight: 700;">{trend}</span>
            </div>
            <h2 style="font-size: 2.2rem; font-weight: 800; margin: 0;">{value}<span style="font-size: 0.9rem; font-weight: 400; color: #bbcabf; margin-left: 5px;">{unit}</span></h2>
            <div style="display: flex; gap: 4px; margin-top: 15px; height: 20px; align-items: flex-end;">
                <div style="background: rgba(78, 222, 163, 0.2); height: 40%; flex: 1; border-radius: 2px;"></div>
                <div style="background: rgba(78, 222, 163, 0.4); height: 70%; flex: 1; border-radius: 2px;"></div>
                <div style="background: rgba(78, 222, 163, 0.6); height: 50%; flex: 1; border-radius: 2px;"></div>
                <div style="background: rgba(78, 222, 163, 0.8); height: 90%; flex: 1; border-radius: 2px;"></div>
                <div style="background: #4edea3; height: 60%; flex: 1; border-radius: 2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col1: kpi_card("EYE HEALTH INDEX", f"{health_score:.1f}", "avg", "↑ +20.0%")
    with col2: kpi_card("SCREEN TIME", f"{st.session_state.screen_time:.1f}", "hrs", "↑ +3.5%")
    with col3:
        st.markdown(f"""
        <div class="glass-panel" style="padding: 20px; border-radius: 16px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <p style="font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #bbcabf;">AI DIAGNOSTICS</p>
                <span style="background: rgba(78, 222, 163, 0.1); color: #4edea3; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 800;">STABLE</span>
            </div>
            <h2 style="font-size: 2.2rem; font-weight: 800; margin: 0;">1.2<span style="font-size: 0.9rem; font-weight: 400; color: #bbcabf; margin-left: 5px;">ms/inf</span></h2>
            <p style="font-size: 12px; color: #6e7a8a; margin-top: 10px;">Model response latency</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="glass-panel" style="padding: 20px; border-radius: 16px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <p style="font-size: 11px; font-weight: 700; letter-spacing: 1px; color: #bbcabf;">ACTIVE MODELS</p>
                <span style="color: #4edea3;">⚙️</span>
            </div>
            <h2 style="font-size: 2.2rem; font-weight: 800; margin: 0;">{st.session_state.active_models}</h2>
            <div style="display: flex; gap: 4px; margin-top: 15px;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #4edea3;"></div>
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #4edea3;"></div>
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #4edea3;"></div>
                <div style="width: 8px; height: 8px; border-radius: 50%; background: rgba(78, 222, 163, 0.2);"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TIER 2: INSIGHTS & CONTROLS ---
    mcol1, mcol2 = st.columns([1, 2], gap="large")

    with mcol1:
        model_insights_html = f"""<div class="glass-panel" style="padding: 20px; border-radius: 16px; min-height: 480px; margin-bottom: 20px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 15px;">
<h3 style="margin: 0; font-size: 1.2rem;">Model Insights</h3>
<span style="color: #6e7a8a;">ℹ️</span>
</div>
<div style="margin-bottom: 25px;">
<div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
<span style="font-size: 13px; font-weight: 600;">Linear Regression</span>
<span style="color: #4edea3; font-weight: 800;">{st.session_state.accuracy}%</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px;">
<div style="width: {st.session_state.accuracy}%; height: 100%; background: #4edea3; border-radius: 10px;"></div>
</div>
<p style="font-size: 11px; color: #6e7a8a; margin-top: 8px;">Accuracy score for refractive error prediction</p>
</div>
<div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 30px;">
<div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
<div style="display: flex; align-items: center; gap: 10px;"><span style="color: #4edea3;">🌐</span> <span style="font-size: 13px;">Neural Weights</span></div>
<span style="font-family: monospace; font-size: 12px; color: #bbcabf;">{st.session_state.model_version}</span>
</div>
<div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
<div style="display: flex; align-items: center; gap: 10px;"><span style="color: #4edea3;">🌲</span> <span style="font-size: 13px;">Decision Trees</span></div>
<span style="font-family: monospace; font-size: 12px; color: #bbcabf;">{st.session_state.active_models} Active</span>
</div>
<div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
<div style="display: flex; align-items: center; gap: 10px;"><span style="color: #4edea3;">⚡</span> <span style="font-size: 13px;">Pruning Rate</span></div>
<span style="font-family: monospace; font-size: 12px; color: #bbcabf;">14.2%</span>
</div>
</div>
</div>"""
        st.write(model_insights_html, unsafe_allow_html=True)
        # Using Streamlit button overlaid conceptually
        st.markdown("<div style='margin-top: -65px;'></div>", unsafe_allow_html=True)
        if st.button("RETRAIN MODEL", use_container_width=True):
            with st.spinner("Retraining..."):
                time.sleep(2)
                retrain_model()
                st.rerun()

    with mcol2:
        mo_status = "ON" if st.session_state.manual_override else "OFF"
        control_panel_html = f"""<div class="glass-panel" style="padding: 20px; border-radius: 16px; min-height: 480px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 15px;">
<h3 style="margin: 0; font-size: 1.2rem;">Diagnostic Control Panel</h3>
<span class="status-pill status-risk">MANUAL OVERRIDE: {mo_status}</span>
</div>
<div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px;">
<div style="display: flex; flex-direction: column; gap: 30px;">
<div style="height: 150px; border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #6e7a8a; font-size: 12px;">Visual Frequency Wavefront [Live]</div>
<div style="height: 150px; border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #6e7a8a; font-size: 12px;">Neural Convergence Map [Sync]</div>
</div>
<div style="display: flex; flex-direction: column; gap: 20px;">
<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; flex: 1;">
<span style="font-size: 10px; font-weight: 800; color: #6e7a8a; display: block; margin-bottom: 5px;">OCULAR DRIFT</span>
<h4 style="margin: 0; font-size: 1.4rem; color: #4edea3;">{drift}</h4>
</div>
<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; flex: 1;">
<span style="font-size: 10px; font-weight: 800; color: #6e7a8a; display: block; margin-bottom: 5px;">TEAR STABILITY</span>
<h4 style="margin: 0; font-size: 1.4rem; color: #4edea3;">{tear}</h4>
</div>
</div>
</div>
</div>"""
        st.write(control_panel_html, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div style='margin-top: -380px;'></div>", unsafe_allow_html=True)
            cleft, cright = st.columns([1.2, 1], gap="large")
            with cleft:
                st.session_state.sleep_val = st.slider("Sleep Duration (hrs)", 4.0, 12.0, st.session_state.sleep_val, 0.5)
                st.session_state.lux_val = st.slider("Luminance Exposure (Lux)", 0, 2000, st.session_state.lux_val, 50)
                st.session_state.screen_time = st.slider("Daily Screen Time (hrs)", 0.0, 16.0, st.session_state.screen_time, 0.2)
                st.session_state.manual_override = st.toggle("Enable Manual Override", value=st.session_state.manual_override)
            with cright:
                st.session_state.vitamin_val = st.number_input("Vitamin A Intake (mcg)", 0, 2000, st.session_state.vitamin_val)
                st.session_state.active_models = st.number_input("Active Models Limit", 1, 30, st.session_state.active_models)

elif st.session_state.current_page in ["Explorer", "Patient Flow"]:
    # --- TIER 3: RAW INTELLIGENCE TABLE ---
    st.markdown("""
    <div class="glass-panel" style="border-radius: 16px; overflow: hidden;">
        <div style="padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3 style="margin: 0; font-size: 1.2rem;">Raw Intelligence Explorer</h3>
                <p style="font-size: 10px; font-weight: 800; color: #6e7a8a; margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;">Historical Patient Metrics</p>
            </div>
            <div style="display: flex; gap: 10px; color: #6e7a8a;">
                <span>🔍</span> <span>📥</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df = st.session_state.patients_df
    if search_term:
        df = df[df['patient_id'].str.contains(search_term, case=False) | df['inf'].str.contains(search_term, case=False)]

    cols = st.columns([1.5, 1, 1, 1.5, 1, 0.5])
    # Table Header
    headers = ["PATIENT ID", "SLEEP (HRS)", "SCREEN (HRS)", "HEALTH INDEX", "INFERENCE", ""]
    for i, h in enumerate(headers):
        cols[i].markdown(f"**{h}**")

    # Table Body
    for idx, p in df.iterrows():
        row = st.columns([1.5, 1, 1, 1.5, 1, 0.5])
        row[0].markdown(f"<span style='color:#4edea3; font-weight:700;'>{p['patient_id']}</span>", unsafe_allow_html=True)
        row[1].text(f"{p['sleep']:.1f}")
        row[2].text(f"{p['screen']:.1f}")
        row[3].markdown(f"""
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 50px; height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                <div style="width: {p['health']}%; height: 100%; background: #4edea3; border-radius: 10px;"></div>
            </div>
            <span style="font-size: 12px; font-weight:bold;">{p['health']}%</span>
        </div>
        """, unsafe_allow_html=True)
        row[4].markdown(f"<div class='status-pill {p['class']}'>{p['inf']}</div>", unsafe_allow_html=True)
        row[5].markdown("🔗")

    st.markdown(f"""
    <div style="padding: 15px 20px; color: #6e7a8a; font-size: 11px; font-weight: 700; letter-spacing: 1px; display: flex; justify-content: space-between;">
        <span>SHOWING {len(df)} OF {len(st.session_state.patients_df)} ENTRIES</span>
        <div>PREVIOUS | NEXT</div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="display: flex; justify-content:center; align-items:center; height: 400px; flex-direction:column; color:#6e7a8a;">
        <h1 style="font-size: 4rem; margin-bottom:10px;">🚧</h1>
        <h2>{st.session_state.current_page}</h2>
        <p>This module is currently under development.</p>
    </div>
    """, unsafe_allow_html=True)
