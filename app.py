import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. Page Configuration
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026 - TV", layout="wide")

# --- SETTINGS ---
# Oya dapu aluth Google Drive Image ID eka
IMAGE_FILE_ID = "1fDnUlHbPnaRcJHsg_OvnVjEdkpCM2WCa"
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
BG_URL = f"https://lh3.googleusercontent.com/u/0/d/{IMAGE_FILE_ID}"

# 2. TV-Optimized Styling (BIG FONTS & TEAM COLORS)
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .main-title {{
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 5px 5px 25px rgba(0,0,0,1);
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 5px;
    }}

    /* Team Specific Metric Colors */
    [data-testid="stMetricValue"] {{ font-size: 100px !important; font-weight: 800; color: white !important; }}
    [data-testid="stMetricLabel"] {{ font-size: 45px !important; font-weight: 700; }}

    /* Custom Metric Card Glass Effect */
    .stMetric {{
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(15px);
        border-radius: 35px !important;
        padding: 30px !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.7);
    }}

    /* Latest Update Section at Bottom */
    .footer-table {{
        background: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.1);
    }}
    
    .stTable {{ font-size: 28px !important; color: white !important; }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data(ttl=5)
def get_live_data():
    try:
        return pd.read_csv(MARKS_URL)
    except:
        return None

df = get_live_data()

if df is not None:
    # Calculating Team Scores
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)
    
    # --- TOP: LIVE STANDINGS (Cards with colors) ---
    st.markdown("<h2 style='text-align: center; color: white; font-size: 40px;'>🥇 LIVE LEADERBOARD</h2>", unsafe_allow_html=True)
    cols = st.columns(len(summary))
    
    # Team colors map
    colors_map = {'Red': '#FF0000', 'Blue': '#1E90FF', 'Green': '#32CD32', 'Yellow': '#FFD700'}

    for i, (idx, row) in enumerate(summary.iterrows()):
        team_name = row['Team ']
        team_color = colors_map.get(team_name.strip(), "#FFFFFF")
        with cols[i]:
            # Injecting team specific color to label
            st.markdown(f"<p style='color:{team_color}; font-size:35px; font-weight:bold; text-align:center; margin-bottom:-50px;'>{team_name}</p>", unsafe_allow_html=True)
            st.metric(label="", value=int(row['Points Added']))

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MIDDLE: POINTS PROGRESS (Vertical Chart - Highlighted) ---
    st.markdown("<h2 style='text-align: center; color: white; font-size: 40px;'>📊 POINTS PROGRESS</h2>", unsafe_allow_html=True)
    fig = px.bar(
        summary, x='Team ', y='Points Added', color='Team ', 
        text='Points Added',
        color_discrete_map=colors_map
    )
    fig.update_layout(
        height=500,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(size=25, color="white"),
        showlegend=False,
        xaxis=dict(title="", showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', visible=False)
    )
    fig.update_traces(
        textfont_size=50, textposition='outside',
        marker_line_color='white', marker_line_width=3
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- BOTTOM: LATEST UPDATES (Table Section) ---
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2)'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FFD700;'>🔔 LATEST SCORE UPDATES</h3>", unsafe_allow_html=True)
    
    recent_activity = df.tail(5).iloc[::-1]
    st.table(recent_activity[['Time', 'Team ', 'Game Name', 'Points Added']])

else:
    st.error("Sheet data load karanna baha!")

# Auto-Refresh
time.sleep(10)
st.rerun()
