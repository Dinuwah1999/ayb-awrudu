import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. Page Configuration (Full Width for TV)
st.set_page_config(page_title="Ayathi Avurudu Udanaya Dashboard", layout="wide")

# --- SETTINGS ---
# Aluth Google Drive Image ID eka
IMAGE_FILE_ID = "1fDnUlHbPnaRcJHsg_OvnVjEdkpCM2WCa"
# Google Sheet URL
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Direct Image Link for Background
BG_URL = f"https://lh3.googleusercontent.com/u/0/d/{IMAGE_FILE_ID}"

# 2. TV-Optimized Styling (BIG FONTS & GLASS UI)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)), 
                    url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .main-title {{
        font-size: 85px !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 6px 6px 25px rgba(0,0,0,1);
        padding-top: 10px;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 4px;
    }}

    /* Score Cards */
    [data-testid="stMetricValue"] {{
        font-size: 110px !important;
        font-weight: 800;
        color: #ffffff !important;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 45px !important;
        font-weight: 700;
        color: #FFD700 !important;
    }}

    .stMetric {{
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(20px);
        border-radius: 40px !important;
        padding: 40px !important;
        box-shadow: 0 20px 60px rgba(0,0,0,0.9);
    }}

    /* Table styling */
    .stTable {{ 
        font-size: 28px !important; 
        background-color: rgba(0,0,0,0.6) !important;
        color: white !important;
        border-radius: 20px;
    }}
    
    /* Hide Default UI */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# 3. Data Loading Logic
@st.cache_data(ttl=5)
def get_live_data():
    try:
        return pd.read_csv(MARKS_URL)
    except:
        return None

df = get_live_data()

if df is not None:
    # Calculating Team-wise Total Scores
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)

    # --- LEADERBOARD ---
    st.write("### 🥇 LIVE STANDINGS")
    cols = st.columns(len(summary))
    for i, (idx, row) in enumerate(summary.iterrows()):
        with cols[i]:
            st.metric(label=row['Team '], value=int(row['Points Added']))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- ADVANCED CHART & RECENT UPDATES ---
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.write("### 📊 POINTS PROGRESS")
        # Vertical Bar chart with customized UI
        fig = px.bar(
            summary, 
            x='Team ', 
            y='Points Added', 
            color='Team ', 
            text='Points Added',
            color_discrete_map={
                'Red': '#FF0000', 'Blue': '#1E90FF', 
                'Green': '#32CD32', 'Yellow': '#FFD700'
            }
        )
        
        fig.update_layout(
            height=550,
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(size=25, color="white"),
            showlegend=False,
            xaxis=dict(title="", showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Total Points")
        )
        fig.update_traces(
            textfont_size=45, 
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("### 📢 LATEST UPDATES")
        recent = df.tail(6).iloc[::-1]
        st.table(recent[['Team ', 'Points Added']])

else:
    st.error("Data load karanna baha. Google Sheet Link eka check karanna!")

# 4. Auto-Refresh (10 Seconds)
time.sleep(10)
st.rerun()
