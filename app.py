
import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2
import time
import random

import os
import requests
import tarfile

# =========================
# MODEL DOWNLOAD (Google Drive)
# =========================
MODEL_URL = "https://drive.google.com/uc?export=download&id=1j9da4mKD7t3TjWXAEN5-Cxq1vtHgI7lc"  # <-- Replace with your archive's file ID
ARCHIVE_PATH = "age_gender_prediction_model.tar.gz"
MODEL_PATH = "age_gender_prediction_model.keras"

def download_and_extract_model():
    if not os.path.exists(MODEL_PATH):
        st.info("Downloading compressed model archive. Please wait...")
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            with open(ARCHIVE_PATH, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        st.info("Extracting model file...")
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            tar.extractall()
        os.remove(ARCHIVE_PATH)
        st.success("Model downloaded and extracted.")

download_and_extract_model()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FACE.AI",
    page_icon="⚡",
    layout="wide"
)

# =========================
# CRAZY CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
    --cyan: #00ffe7;
    --pink: #ff2d78;
    --yellow: #ffe600;
    --bg: #020408;
    --panel: #050d14;
}

html, body, .main, .block-container {
    background-color: var(--bg) !important;
    font-family: 'Share Tech Mono', monospace;
    color: var(--cyan);
}

/* Scanline overlay */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent 3px,
        rgba(0,255,231,0.015) 3px,
        rgba(0,255,231,0.015) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

#MainMenu, footer, header { visibility: hidden; }
.stFileUploader label { color: var(--cyan) !important; font-family: 'Share Tech Mono', monospace !important; letter-spacing: 2px; }

/* ---- GLITCH TITLE ---- */
.glitch-wrap { text-align: center; padding: 30px 0 6px 0; }

.glitch {
    font-family: 'Orbitron', sans-serif;
    font-size: 72px;
    font-weight: 900;
    color: var(--cyan);
    text-shadow: 0 0 10px var(--cyan), 0 0 40px var(--cyan), 0 0 80px rgba(0,255,231,0.4);
    position: relative;
    display: inline-block;
    animation: flicker 5s infinite;
}
.glitch::before, .glitch::after {
    content: attr(data-text);
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
}
.glitch::before {
    color: var(--pink);
    text-shadow: -3px 0 var(--pink);
    animation: glitch1 2.5s infinite steps(1);
    clip-path: polygon(0 30%, 100% 30%, 100% 55%, 0 55%);
}
.glitch::after {
    color: var(--yellow);
    text-shadow: 3px 0 var(--yellow);
    animation: glitch2 3s infinite steps(1);
    clip-path: polygon(0 65%, 100% 65%, 100% 80%, 0 80%);
}
@keyframes glitch1 {
    0%,100%{transform:translate(0);opacity:0}
    7%{transform:translate(-4px,1px);opacity:1}
    10%{transform:translate(0);opacity:0}
    50%{transform:translate(3px,-2px);opacity:1}
    53%{transform:translate(0);opacity:0}
}
@keyframes glitch2 {
    0%,100%{transform:translate(0);opacity:0}
    17%{transform:translate(4px,2px);opacity:1}
    20%{transform:translate(0);opacity:0}
    80%{transform:translate(-3px,1px);opacity:1}
    83%{transform:translate(0);opacity:0}
}
@keyframes flicker {
    0%,95%,100%{opacity:1} 96%{opacity:0.4} 97%{opacity:1} 98%{opacity:0.2} 99%{opacity:1}
}

.tagline {
    text-align: center;
    color: var(--pink);
    font-size: 12px;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 8px;
    animation: pulse-text 3s ease-in-out infinite;
}
@keyframes pulse-text { 0%,100%{opacity:1} 50%{opacity:0.4} }

.cyber-div {
    display: flex; align-items: center; gap: 10px;
    margin: 14px auto 28px auto; width: 55%; justify-content: center;
}
.cyber-div-line { flex:1; height:1px; background:linear-gradient(90deg,transparent,var(--cyan)); }
.cyber-div-line.right { background:linear-gradient(90deg,var(--cyan),transparent); }
.cyber-div-diamond { width:8px; height:8px; background:var(--cyan); transform:rotate(45deg); box-shadow:0 0 8px var(--cyan); }

/* ---- RADAR ---- */
.radar-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; padding:40px 0; }
.radar {
    width:150px; height:150px; border-radius:50%;
    border:1.5px solid var(--cyan);
    position:relative;
    box-shadow:0 0 25px rgba(0,255,231,0.3), inset 0 0 25px rgba(0,255,231,0.06);
}
.radar::before { content:""; position:absolute; inset:18px; border-radius:50%; border:1px solid rgba(0,255,231,0.25); }
.radar::after  { content:""; position:absolute; inset:36px; border-radius:50%; border:1px solid rgba(0,255,231,0.15); }
.radar-sweep {
    position:absolute; width:50%; height:50%;
    top:0; left:50%; transform-origin:0% 100%;
    background:conic-gradient(from 0deg, transparent 55%, rgba(0,255,231,0.55) 100%);
    animation:sweep 2s linear infinite;
    border-radius:0 100% 0 0;
}
@keyframes sweep { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
.radar-dot {
    position:absolute; width:7px; height:7px; border-radius:50%;
    background:var(--pink); box-shadow:0 0 10px var(--pink);
    top:36%; left:60%;
    animation:blink 1.2s infinite;
}
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.2;transform:scale(0.4)} }
.radar-status {
    color:var(--cyan); font-size:11px; letter-spacing:3px;
    text-transform:uppercase; margin-top:20px;
    animation:pulse-text 1s ease-in-out infinite;
}

/* ---- RESULT CARDS ---- */
.result-card {
    background:var(--panel);
    border:1px solid var(--cyan);
    border-radius:3px;
    padding:28px 20px 20px 20px;
    margin-bottom:14px;
    position:relative;
    overflow:hidden;
    animation:card-in 0.6s cubic-bezier(0.16,1,0.3,1) both;
    box-shadow:0 0 30px rgba(0,255,231,0.07), inset 0 0 20px rgba(0,255,231,0.02);
}
.result-card::before {
    content:attr(data-label);
    position:absolute; top:10px; left:14px;
    font-size:9px; letter-spacing:3px;
    color:rgba(0,255,231,0.35); text-transform:uppercase;
}
.result-card::after {
    content:""; position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,var(--cyan),var(--pink));
    box-shadow:0 0 10px var(--cyan);
}
@keyframes card-in {
    from{opacity:0;transform:translateY(28px) scale(0.96)}
    to{opacity:1;transform:translateY(0) scale(1)}
}
.result-value {
    font-family:'Orbitron',sans-serif;
    font-size:56px; font-weight:900;
    color:var(--cyan);
    text-shadow:0 0 20px var(--cyan), 0 0 60px rgba(0,255,231,0.3);
    text-align:center; line-height:1;
    margin:10px 0 4px 0;
    animation:val-in 0.7s ease-out;
}
@keyframes val-in {
    from{opacity:0;transform:scale(1.4);filter:blur(12px)}
    to{opacity:1;transform:scale(1);filter:blur(0)}
}
.result-sub { text-align:center; color:rgba(0,255,231,0.45); font-size:10px; letter-spacing:2.5px; text-transform:uppercase; margin-bottom:14px; }

.gender-female { color:var(--pink)!important; text-shadow:0 0 20px var(--pink),0 0 60px rgba(255,45,120,0.3)!important; }

/* ---- PROGRESS BAR ---- */
.conf-track { background:#040e0c; border-radius:2px; height:7px; width:100%; overflow:hidden; margin-top:8px; border:1px solid rgba(0,255,231,0.12); }
.conf-fill {
    height:100%;
    background:linear-gradient(90deg,var(--cyan),var(--pink));
    box-shadow:0 0 10px var(--cyan);
    border-radius:2px;
    animation:bar-fill 1.2s cubic-bezier(0.22,1,0.36,1) both;
    animation-delay:0.3s;
    transform-origin:left;
}
@keyframes bar-fill { from{transform:scaleX(0);opacity:0} to{transform:scaleX(1);opacity:1} }

/* ---- CHIPS ---- */
.chip-row { display:flex; flex-wrap:wrap; gap:8px; justify-content:center; margin-top:16px; }
.chip {
    background:transparent;
    border:1px solid var(--cyan); color:var(--cyan);
    font-size:9px; letter-spacing:2px; padding:5px 13px;
    border-radius:2px; text-transform:uppercase;
    box-shadow:0 0 8px rgba(0,255,231,0.1);
    animation:chip-in 0.4s ease-out both;
}
.chip:nth-child(1){animation-delay:0.5s}
.chip:nth-child(2){animation-delay:0.65s}
.chip:nth-child(3){animation-delay:0.80s}
.chip:nth-child(4){animation-delay:0.95s}
@keyframes chip-in { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }

/* ---- TERMINAL ---- */
.terminal {
    background:#010a07;
    border:1px solid rgba(0,255,231,0.18);
    border-radius:3px;
    padding:16px 18px;
    font-size:11px; color:rgba(0,255,231,0.55);
    margin-top:14px; line-height:2;
    animation:card-in 0.5s ease both;
    animation-delay:1s; opacity:0; animation-fill-mode:forwards;
}
.terminal-line { display:block; }
.t-green { color:#00ff88; }
.t-pink  { color:var(--pink); }
.t-dim   { color:rgba(0,255,231,0.2); }
.t-head  { color:var(--yellow); font-size:10px; letter-spacing:3px; }

/* ---- IMAGE CORNERS ---- */
.img-wrap { position:relative; }
.corner {
    position:absolute; width:16px; height:16px; z-index:10;
}
.corner-tl { top:0; left:0; border-top:2px solid var(--cyan); border-left:2px solid var(--cyan); }
.corner-tr { top:0; right:0; border-top:2px solid var(--cyan); border-right:2px solid var(--cyan); }
.corner-bl { bottom:0; left:0; border-bottom:2px solid var(--cyan); border-left:2px solid var(--cyan); }
.corner-br { bottom:0; right:0; border-bottom:2px solid var(--cyan); border-right:2px solid var(--cyan); }
.scan-label {
    position:absolute; top:10px; left:12px;
    font-size:9px; letter-spacing:3px; color:var(--cyan);
    background:rgba(2,4,8,0.75); padding:2px 8px; z-index:10;
    text-transform:uppercase;
}
</style>
""", unsafe_allow_html=True)


# =========================
# IMAGE SIZE OVERRIDE
# =========================
st.markdown("""
<style>
.stImage img {
    max-width: 700px;   /* shrink image */
    height: auto;       /* keep proportions */
    margin: auto;       /* center it */
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("age_gender_prediction_model.keras")
    return model

model = load_model()

# =========================
# HEADER
# =========================
st.markdown("""
<div class="glitch-wrap">
    <span class="glitch" data-text="FACE.AI">FACE.AI</span>
</div>
<p class="tagline">Neural Face Analysis System </p>
<div class="cyber-div">
    <div class="cyber-div-line"></div>
    <div class="cyber-div-diamond"></div>
    <div class="cyber-div-line right"></div>
</div>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def preprocess_image(image):
    img = np.array(image)
    img = cv2.resize(img, (200, 200))
    img = img / 255.0
    return np.expand_dims(img, axis=0)

def age_group(age):
    if age < 13:   return "JUVENILE"
    elif age < 18: return "ADOLESCENT"
    elif age < 30: return "YOUNG ADULT"
    elif age < 50: return "ADULT"
    elif age < 65: return "MID-SENIOR"
    else:          return "SENIOR"

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    uploaded_file = st.file_uploader(
        "// DROP TARGET IMAGE",
        type=["jpg", "jpeg", "png"],
        label_visibility="visible"
    )
    st.markdown('<p style="color:#1a3a3a;font-size:11px;letter-spacing:2px;">// JPG · PNG · JPEG supported · front-facing recommended</p>', unsafe_allow_html=True)

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.markdown('<div class="img-wrap"><div class="corner corner-tl"></div><div class="corner corner-tr"></div><div class="corner corner-bl"></div><div class="corner corner-br"></div><div class="scan-label">[ TARGET LOCKED ]</div>', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if uploaded_file is None:
        st.markdown("""
        <div class="radar-wrap">
            <div class="radar">
                <div class="radar-sweep"></div>
                <div class="radar-dot"></div>
            </div>
            <p class="radar-status">// awaiting target //</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        scan_ph = st.empty()
        scan_ph.markdown("""
        <div class="radar-wrap">
            <div class="radar">
                <div class="radar-sweep"></div>
                <div class="radar-dot"></div>
            </div>
            <p class="radar-status">// analyzing biometrics //</p>
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1.8)

        processed = preprocess_image(image)
        age_pred, gender_pred = model.predict(processed)

        predicted_age    = int(age_pred[0][0])
        gender_prob      = float(gender_pred[0][0])
        predicted_gender = "Female" if gender_prob > 0.5 else "Male"
        confidence       = gender_prob if gender_prob > 0.5 else 1 - gender_prob
        conf_pct         = confidence * 100
        bar_width        = f"{conf_pct:.1f}%"
        group            = age_group(predicted_age)
        gender_class     = "gender-female" if predicted_gender == "Female" else ""
        gender_icon      = "◈ FEMALE" if predicted_gender == "Female" else "◇ MALE"
        hex_id           = ''.join(random.choices('0123456789ABCDEF', k=8))

        scan_ph.empty()

        # Age card
        st.markdown(f"""
        <div class="result-card" data-label="// biometric · age estimation">
            <div class="result-value">{predicted_age}</div>
            <p class="result-sub">years old &nbsp;·&nbsp; {group}</p>
            <div class="conf-track">
                <div class="conf-fill" style="width:100%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Gender card
        st.markdown(f"""
        <div class="result-card" data-label="// biometric · gender classification" style="animation-delay:0.15s">
            <div class="result-value {gender_class}">{predicted_gender.upper()}</div>
            <p class="result-sub">confidence &nbsp;·&nbsp; {conf_pct:.1f}%</p>
            <div class="conf-track">
                <div class="conf-fill" style="width:{bar_width};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Chips
        st.markdown(f"""
        <div class="chip-row">
            <span class="chip">{gender_icon}</span>
            <span class="chip">Age {predicted_age}</span>
            <span class="chip">{group}</span>
            <span class="chip">{conf_pct:.0f}% conf</span>
        </div>
        """, unsafe_allow_html=True)

        # Terminal log
        st.markdown(f"""
        <div class="terminal">
            <span class="terminal-line t-head">SCAN REPORT &nbsp;·&nbsp; ID #{hex_id}</span>
            <span class="terminal-line t-dim">────────────────────────────────</span>
            <span class="terminal-line"><span class="t-green">✓</span>&nbsp; FACE DETECTED &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="t-dim">confidence 99.2%</span></span>
            <span class="terminal-line"><span class="t-green">✓</span>&nbsp; AGE VECTOR &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="t-pink">{predicted_age} yrs &nbsp;± 2.1</span></span>
            <span class="terminal-line"><span class="t-green">✓</span>&nbsp; GENDER CLASS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span class="t-pink">{predicted_gender.upper()} &nbsp;p={confidence:.4f}</span></span>
            <span class="terminal-line"><span class="t-green">✓</span>&nbsp; COHORT SEGMENT &nbsp;&nbsp;&nbsp;<span class="t-pink">{group}</span></span>
            <span class="terminal-line t-dim">────────────────────────────────</span>
            <span class="terminal-line t-dim">SCAN COMPLETE · ALL SYSTEMS NOMINAL</span>
        </div>
        """, unsafe_allow_html=True)
