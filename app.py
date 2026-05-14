import streamlit as st
import pandas as pd
import plotly.express as px
import time
import base64

# Page configuration
st.set_page_config(page_title="Ayathi Avurudu Udanaya - TV", layout="wide")

# --- BACKGROUND IMAGE FUNCTION ---
def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{b64_encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* 50% Overlay readability ekata */
        z-index: -1;
    }}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# 1. Background eka set karanna (Oyaage JPG file name eka methanata danna)
try:
    set_background("image_b10cfb.jpg") 
except:
    st.warning("Background image eka hambune na. GitHub ekata upload karala thiyeda balanna.")

# --- TV STYLING (BIG FONTS) ---
st.markdown("""
    <style>
    .main-title {
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 5px 5px 15px rgba(0,0,0,0.9);
        margin-top: -50px;
    }
    [data-testid="stMetricValue"] { font-size: 85px !important; font-weight: bold; color: white !important; }
    [data-testid="stMetricLabel"] { font-size: 35px !important; color: #FFD700 !important; }
    .stMetric {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 30px !important;
        padding: 40px !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* Hide menus */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# Data fetching logic
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=5) # 5 seconds cache
def get_live_data():
    return pd.read_csv(MARKS_URL)

try:
    df = get_live_data()
    # Team Summary calculation from Marks Entry [cite: 1]
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)

    # Leaderboard Cards
    st.write("### 🥇 LIVE SCORE")
    cols = st.columns(len(summary))
    for i, (idx, row) in enumerate(summary.iterrows()):
        with cols[i]:
            st.metric(label=row['Team '], value=int(row['Points Added']))

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    c1, c2 = st.columns([2, 1])
    with c1:
        fig = px.bar(summary, x='Team ', y='Points Added', color='Team ', text='Points Added',
                     color_discrete_map={'Red':'#FF4B4B', 'Blue':'#1F77B4', 'Green':'#2CA02C', 'Yellow':'#FFD700'})
        fig.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          font=dict(size=20, color="white"), showlegend=False)
        fig.update_traces(textfont_size=30, textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("### 📢 RECENT UPDATES")
        st.table(df.tail(5)[['Team ', 'Points Added']].iloc[::-1])

except Exception as e:
    st.write("Waiting for data...")

# Auto Refresh 10s
time.sleep(10)
st.rerun()
