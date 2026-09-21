import streamlit as st
import pandas as pd
import joblib
import subprocess
import re
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="IDS SOC - SCADA/ICS Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS PERSONNALISÉ (Style SOC/Dark Theme) =====
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    h1, h2, h3 {
        color: #00ff9f !important;
        font-family: 'Courier New', monospace;
    }
    div[data-testid="stMetricValue"] {
        color: #00ff9f;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #8b92a1;
    }
    .status-banner {
        background: linear-gradient(90deg, #0e1117 0%, #1a1d24 50%, #0e1117 100%);
        border-left: 4px solid #00ff9f;
        padding: 10px 20px;
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background-color: #00ff9f;
        color: #0e1117;
        font-weight: bold;
        border-radius: 4px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00cc7f;
        color: #0e1117;
    }
</style>
""", unsafe_allow_html=True)

# ===== HEADER SOC STYLE =====
current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

st.markdown(f"""
<div class="status-banner">
    <span style="color:#00ff9f; font-size:24px; font-weight:bold;">🛡️ SOC — SECURITY OPERATIONS CENTER</span><br>
    <span style="color:#8b92a1; font-family:'Courier New';">IDS Intelligent | Protocoles Industriels SCADA/ICS | Session: {current_time}</span>
</div>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🖥️ SYSTEM STATUS")
    st.success("🟢 Conpot (PLC) : ONLINE")
    st.success("🟢 ML Engine : ACTIVE")
    st.success("🟢 Ollama LLM : ACTIVE")
    st.markdown("---")
    st.markdown("### 📡 MONITORED TARGET")
    st.code("IP: 192.168.37.137\nPort: 502 (Modbus)\nProtocol: Modbus TCP", language=None)
    st.markdown("---")
    st.markdown("### ℹ️ MODEL INFO")
    st.text("Algorithm: Random Forest")
    st.text("Accuracy: 100%")
    st.text("Features: 4")

# Charger les données et le modèle
@st.cache_data
def load_data():
    return pd.read_csv('final_dataset.csv')

@st.cache_resource
def load_model():
    return joblib.load('ids_model.pkl')

df = load_data()
model = load_model()

# ===== SECTION 1 : KPI CARDS =====
st.markdown("### 📊 THREAT OVERVIEW")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("TOTAL EVENTS", f"{len(df):,}")
with col2:
    st.metric("NORMAL TRAFFIC", f"{len(df[df['label']==0]):,}", delta="Safe", delta_color="normal")
with col3:
    st.metric("THREATS DETECTED", f"{len(df[df['label']==1]):,}", delta="Alert", delta_color="inverse")
with col4:
    threat_ratio = round(len(df[df['label']==1]) / len(df) * 100, 1)
    st.metric("THREAT RATIO", f"{threat_ratio}%")

st.markdown("---")

# ===== SECTION 2 : GRAPHIQUES =====
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎯 Distribution des Événements")
    label_counts = df['label'].map({0: 'Normal', 1: 'Malicious'}).value_counts()
    fig1 = go.Figure(data=[go.Pie(
        labels=label_counts.index,
        values=label_counts.values,
        marker=dict(colors=['#00ff9f', '#ff3860']),
        hole=0.5
    )])
    fig1.update_layout(
        paper_bgcolor='#0e1117',
        plot_bgcolor='#0e1117',
        font=dict(color='#8b92a1'),
        showlegend=True,
        height=350
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### ⏱️ Analyse Temporelle (time_delta)")
    fig2 = go.Figure()
    for label, name, color in [(0, 'Normal', '#00ff9f'), (1, 'Malicious', '#ff3860')]:
        subset = df[df['label']==label]['time_delta']
        fig2.add_trace(go.Box(y=subset, name=name, marker_color=color))
    fig2.update_layout(
        paper_bgcolor='#0e1117',
        plot_bgcolor='#1a1d24',
        font=dict(color='#8b92a1'),
        height=350
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ===== SECTION 3 : LIVE THREAT ANALYSIS =====
st.markdown("### 🔍 LIVE THREAT ANALYSIS")
st.markdown("Simuler et analyser une requête réseau en temps réel")

col1, col2, col3, col4 = st.columns(4)
function_code = col1.selectbox("Function Code", [3, 6], help="3=Read, 6=Write")
address = col2.number_input("Address", value=40001)
device_id = col3.number_input("Device ID", value=2)
time_delta = col4.number_input("Time Delta (sec)", value=0.5, step=0.1)

if st.button("▶ LANCER L'ANALYSE", type="primary"):
    new_request = pd.DataFrame([{
        'function_code': function_code,
        'address': address,
        'device_id': device_id,
        'time_delta': time_delta
    }])

    prediction = model.predict(new_request)[0]
    proba = model.predict_proba(new_request)[0]

    if prediction == 1:
        st.markdown(f"""
        <div style="background-color:#2d0a0f; border-left:4px solid #ff3860; padding:15px; border-radius:4px;">
        <span style="color:#ff3860; font-size:20px; font-weight:bold;">🚨 ALERTE CRITIQUE — TRAFIC MALVEILLANT DÉTECTÉ</span><br>
        <span style="color:#8b92a1;">Confiance du modèle : {proba[1]*100:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("🤖 Analyse par l'IA (Ollama) en cours..."):
            prompt = f"""Tu es un expert en cybersécurité industrielle (SCADA/ICS/Modbus).

Une alerte a été détectée par un système IDS basé sur du Machine Learning :

- Function Code : {function_code} ({'Write Register (écriture non-autorisée)' if function_code==6 else 'Read Register (lecture)'})
- Adresse mémoire ciblée : {address}
- ID de l'appareil (device_id) : {device_id}
- Intervalle entre requêtes : {time_delta} secondes
- Classification du modèle ML : MALICIOUS (confiance {proba[1]*100:.1f}%)

IMPORTANT : Le Function Code est un type d'operation Modbus standard (3=lecture, 6=ecriture), pas une fonctionnalite qu'on peut desactiver individuellement. Ne recommande pas de desactiver le code X. A la place, recommande des actions concretes comme : isoler l'appareil du reseau, bloquer l'IP source au niveau du pare-feu, desactiver temporairement l'acces en ecriture au PLC, ou auditer les journaux reseau.

Explique en langage clair et technique :
1. Ce qui s'est probablement passe
2. Le niveau de gravite (faible/moyen/eleve)
3. Une action recommandee immediate (parmi les actions valides ci-dessus)

Reponds en francais, de facon concise (5-6 lignes maximum)."""

            result = subprocess.run(
                ['ollama', 'run', 'llama3.2', prompt],
                capture_output=True,
                text=True
            )

            clean_output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', result.stdout)
            clean_output = re.sub(r'\[[0-9]+[DK]', '', clean_output)
            clean_output = clean_output.strip()

        st.markdown("#### 💡 RAPPORT D'ANALYSE IA")
        st.markdown(f"""
        <div style="background-color:#1a1d24; border:1px solid #2d3139; padding:15px; border-radius:4px; color:#e0e0e0;">
        {clean_output.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
        <div style="background-color:#0a2d1a; border-left:4px solid #00ff9f; padding:15px; border-radius:4px;">
        <span style="color:#00ff9f; font-size:20px; font-weight:bold;">✅ TRAFIC NORMAL — AUCUNE MENACE</span><br>
        <span style="color:#8b92a1;">Confiance du modèle : {proba[0]*100:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<span style='color:#4a4f5a; font-size:12px;'>Projet PFE — IDS Intelligent pour Protocoles Industriels (SCADA/ICS) | Machine Learning + IA Générative</span>", unsafe_allow_html=True)
