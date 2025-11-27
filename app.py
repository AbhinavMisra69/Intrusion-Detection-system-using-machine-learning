import streamlit as st
import pandas as pd
import numpy as np
import time
import joblib
from datetime import datetime

# --- 0. PAGE CONFIG ---
st.set_page_config(
    page_title="CYBER_SENTINEL_V4",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 1. ADVANCED CYBER CSS ---
# --- 1. ADVANCED CYBER CSS ---
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
        
        @keyframes gradient-animation {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        
        .stApp {
            background: linear-gradient(-45deg, #020202, #0a0f1c, #1a0b1c, #000000);
            background-size: 400% 400%;
            animation: gradient-animation 15s ease infinite;
            color: #e0e0e0;
            font-family: 'Share Tech Mono', monospace;
        }

        /* REMOVED THE LINE THAT HID THE SIDEBAR */
        /* [data-testid="stSidebar"] {display: none;}  <-- DELETE THIS LINE */
        
        /* Optional: Style the sidebar background to match the theme */
        [data-testid="stSidebar"] {
            background-color: #050505;
            border-right: 1px solid #00ff41;
        }

        header {visibility: hidden;}
        footer {visibility: hidden;}

        .hud-card {
            background: rgba(10, 15, 20, 0.75);
            border: 1px solid rgba(0, 255, 65, 0.3);
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.1);
            border-radius: 4px;
            padding: 20px;
            margin-bottom: 15px;
            backdrop-filter: blur(5px);
            position: relative;
        }
        
        .hud-card::before {
            content: ""; position: absolute; top: -1px; left: -1px; width: 15px; height: 15px;
            border-top: 2px solid #00ff41; border-left: 2px solid #00ff41;
        }
        .hud-card::after {
            content: ""; position: absolute; bottom: -1px; right: -1px; width: 15px; height: 15px;
            border-bottom: 2px solid #00ff41; border-right: 2px solid #00ff41;
        }

        h1, h2, h3 { font-family: 'Orbitron', sans-serif; text-transform: uppercase; letter-spacing: 3px; }
        .neon-text-green { color: #00ff41; text-shadow: 0 0 8px rgba(0, 255, 65, 0.6); }
        .neon-text-red { color: #ff0055; text-shadow: 0 0 8px rgba(255, 0, 85, 0.6); }

        [data-testid="stFileUploader"] { border: 1px dashed #444; padding: 10px; background: rgba(0,0,0,0.5); border-radius: 4px; }

        .cyber-terminal {
            background-color: #050505; border: 1px solid #333; color: #00ff41;
            font-family: 'Share Tech Mono', monospace; padding: 15px; height: 350px;
            overflow-y: auto; box-shadow: inset 0 0 20px rgba(0,0,0,0.8); font-size: 0.85rem;
        }
        .cyber-terminal::-webkit-scrollbar { width: 8px; }
        .cyber-terminal::-webkit-scrollbar-track { background: #000; }
        .cyber-terminal::-webkit-scrollbar-thumb { background: #333; }

        .stButton>button {
            background: transparent; border: 2px solid #00ff41; color: #00ff41;
            font-family: 'Orbitron', sans-serif; width: 100%; transition: all 0.3s ease;
        }
        .stButton>button:hover { background: #00ff41; color: #000; box-shadow: 0 0 20px rgba(0, 255, 65, 0.5); }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- 2. REAL MODEL INTEGRATION ---
@st.cache_resource
def load_resources():
    try:
        # We try to load the files, but we will use a safe fallback map if needed
        model = joblib.load('ids_model.pkl')
        features = joblib.load('selected_features.pkl')
        return model, features
    except FileNotFoundError:
        return None, None

model, selected_features = load_resources()

# --- 3. HELPER FUNCTIONS ---
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def render_metric_card(label, value, is_danger=False):
    color_class = "neon-text-red" if is_danger else "neon-text-green"
    border_color = "#ff0055" if is_danger else "#00ff41"
    st.markdown(f"""
    <div class="hud-card" style="text-align: center; border-color: {border_color};">
        <div style="font-size: 0.8rem; color: #aaa; letter-spacing: 1px;">{label}</div>
        <div class="{color_class}" style="font-size: 2.2rem; font-family: 'Orbitron';">{value}</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. HEADER AREA ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown("<h1 class='neon-text-green'>CYBER // SENTINEL</h1>", unsafe_allow_html=True)
    st.markdown("<div style='letter-spacing: 2px; color: #888;'>AI-DRIVEN TRAFFIC ANALYSIS NODE</div>", unsafe_allow_html=True)
with c2:
    t = datetime.now().strftime('%H:%M:%S UTC')
    status_color = "#00ff41" if model else "#ff0055"
    status_text = "SYSTEM ONLINE" if model else "MODEL OFFLINE"
    st.markdown(f"""
        <div style='text-align: right; border-right: 4px solid {status_color}; padding-right: 15px;'>
            <div style='font-size: 1.5rem; font-family: Orbitron;'>{t}</div>
            <div style='color: {status_color};'>{status_text}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. COMMAND DECK ---
if model is None:
    st.error("⚠️ CRITICAL ERROR: Model files not found. Please export .pkl files from Jupyter Notebook.")
else:
    st.markdown("<h3 class='neon-text-green'>// COMMAND DECK</h3>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="hud-card">', unsafe_allow_html=True)
        col_upload, col_action = st.columns([2, 1])
        
        with col_upload:
            uploaded_file = st.file_uploader("INGEST TRAFFIC LOGS (CSV)", type=['csv'])
        
        with col_action:
            st.write("") 
            st.write("")
            start_btn = st.button("INITIALIZE SCAN SEQUENCE")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. SCANNING LOGIC ---
    if uploaded_file and start_btn:
        st.markdown("<h3 class='neon-text-green'>// LIVE MONITORING GRID</h3>", unsafe_allow_html=True)
        
        # Layout
        m1, m2, m3 = st.columns(3)
        with m1: metric_placeholder_1 = st.empty()
        with m2: metric_placeholder_2 = st.empty()
        with m3: metric_placeholder_3 = st.empty()
        
        c_term, c_graph = st.columns([1.5, 1])
        with c_term: terminal_placeholder = st.empty()
        with c_graph: chart_placeholder = st.empty()

        # Load Data
        df = pd.read_csv(uploaded_file)
        
        # --- SMART COLUMN MATCHING ---
        model_columns = selected_features
        csv_columns = df.columns
        
        # Match case-insensitive/stripped column names
        col_map = {}
        for m_col in model_columns:
            match = None
            for c_col in csv_columns:
                if m_col.strip().lower() == c_col.strip().lower():
                    match = c_col
                    break
            if match:
                col_map[m_col] = match
        
        try:
            X_input = pd.DataFrame()
            for m_col in model_columns:
                if m_col in col_map:
                    X_input[m_col] = df[col_map[m_col]]
                else:
                    X_input[m_col] = 0.0 # Fill missing with 0
            
            X_input = X_input.fillna(0)
            
        except Exception as e:
            st.error(f"Data Processing Error: {e}")
            st.stop()

        # Manual Label Map for Reliability
        SAFE_LABEL_MAP = {
            0: "BENIGN",
            1: "Bot", 2: "BruteForce", 3: "DoS",
            4: "Infiltration", 5: "PortScan", 6: "WebAttack"
        }

        logs_html = ""
        packets = 0
        threats = 0
        threat_log_data = [] 

        # Processing Loop
        chunk_size = 10
        
        for i in range(0, len(X_input), chunk_size):
            X_chunk = X_input.iloc[i:i+chunk_size]
            
            # Predict
            preds = model.predict(X_chunk)
            
            for j, pred_code in enumerate(preds):
                packets += 1
                timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                
                label = SAFE_LABEL_MAP.get(int(pred_code), "Unknown")
                
                if label != "BENIGN":
                    threats += 1
                    log_line = f"<span style='color:#ff0055;'>[ALERT] {timestamp} :: DETECTED: {label} :: PKT_{packets}</span>"
                    
                    # Attempt to get IP data safely
                    src_ip = df.iloc[i+j].get('Source IP', '192.168.1.X')
                    dst_ip = df.iloc[i+j].get('Destination IP', '10.0.0.1')

                    threat_log_data.append({
                        "Timestamp": timestamp,
                        "Packet_ID": packets,
                        "Threat_Type": label,
                        "Source_IP": src_ip,
                        "Destination_IP": dst_ip
                    })
                else:
                    log_line = f"<span style='color:#00ff41;'>[INFO]  {timestamp} :: {label} :: PKT_{packets}</span>"
                
                logs_html = f"<div>{log_line}</div>" + logs_html
                if len(logs_html) > 15000: logs_html = logs_html[:15000]

            # Update UI
            with m1: render_metric_card("PACKETS SCANNED", packets)
            with m2: render_metric_card("THREATS DETECTED", threats, is_danger=(threats>0))
            
            integrity = max(0, 100 - int((threats / max(1, packets)) * 100))
            with m3: render_metric_card("INTEGRITY SCORE", f"{integrity}%", is_danger=(integrity<60))

            terminal_placeholder.markdown(f"""
            <div class="cyber-terminal">
                <div style="margin-bottom: 10px; border-bottom: 1px dashed #333;">ROOT@SENTINEL:~# tail -f /var/log/traffic</div>
                {logs_html}
            </div>
            """, unsafe_allow_html=True)
            
            # Update Chart
            if packets > 0:
                chart_data = pd.DataFrame({
                    "SAFE": [packets - threats],
                    "THREAT": [threats]
                })
                with chart_placeholder:
                    st.bar_chart(chart_data, color=["#00ff41", "#ff0055"])
            
            time.sleep(0.05)

        st.success("SCAN COMPLETE.")
        
        # --- 7. REPORT GENERATION ---
        if threats > 0:
            st.markdown("---")
            st.subheader("🚨 FORENSIC EVIDENCE ACQUIRED")
            
            report_df = pd.DataFrame(threat_log_data)
            csv = convert_df_to_csv(report_df)
            
            st.download_button(
                label="DOWNLOAD FORENSIC REPORT (CSV)",
                data=csv,
                file_name='forensic_report_sentinel.csv',
                mime='text/csv',
            )
            
            with st.expander("VIEW THREAT LOGS"):
                st.dataframe(report_df)

    elif not uploaded_file:
        # Empty State
        st.markdown("""
        <div style='text-align: center; margin-top: 50px; opacity: 0.5;'>
            <h2 style='color: #444; font-family: Orbitron;'>AWAITING DATA STREAM</h2>
            <div>Upload a CSV file in the Command Deck to begin operations.</div>
        </div>
        """, unsafe_allow_html=True)

# --- SIDEBAR CONTENT (Instructions) ---
with st.sidebar:
    st.markdown("""
    <div style="
        color: #00ff41; 
        font-family: 'Share Tech Mono', monospace; 
        border: 1px solid #00ff41; 
        padding: 15px; 
        border-radius: 5px; 
        background: rgba(0, 20, 0, 0.5);
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
    ">
        <h3 style="
            margin-top: 0; 
            border-bottom: 1px dashed #00ff41; 
            padding-bottom: 5px;
            text-shadow: 0 0 5px rgba(0,255,65,0.5);
        ">// OPERATIONAL GUIDE</h3>
        
        <ol style="padding-left: 20px; margin-top: 10px;">
            <li style="margin-bottom: 10px;">
                <strong>INGEST DATA:</strong><br>
                Upload <code>scaled_simulation.csv</code> to the Command Deck.
            </li>
            <li style="margin-bottom: 10px;">
                <strong>CALIBRATE:</strong><br>
                Adjust scan speed via the slider.
            </li>
            <li style="margin-bottom: 10px;">
                <strong>EXECUTE:</strong><br>
                Click <span style="border: 1px solid #00ff41; padding: 0 4px; font-size: 0.8em;">INITIALIZE</span> to begin packet inspection.
            </li>
            <li>
                <strong>FORENSICS:</strong><br>
                Download threat logs if attacks are detected.
            </li>
        </ol>
        
        <div style="
            margin-top: 20px; 
            text-align: center; 
            font-size: 0.8em; 
            opacity: 0.7; 
            border-top: 1px dashed #00ff41; 
            padding-top: 10px;
        ">
            SENTINEL v4.0 SYSTEM<br>
            SECURE CONNECTION ESTABLISHED
        </div>
    </div>
    """, unsafe_allow_html=True)