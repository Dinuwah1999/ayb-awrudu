import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. Page Configuration (Full Width for TV)
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026 - Live", layout="wide")

# --- SETTINGS ---
# Oya dapu Google Drive Image ID eka
IMAGE_FILE_ID = "1EvbUkb77UY148PlcMht3XTxK4WRvOCmV"
# Google Sheet URL
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Direct Image Link for Background
BG_URL = f"https://lh3.googleusercontent.com/u/0/d/{IMAGE_FILE_ID}"

# 2. TV-Optimized Styling (BIG FONTS & BOLD COLORS)
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
        font-size: 90px !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 5px 5px 20px rgba(0,0,0,1);
        padding-top: 10px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 5px;
    }}

    /* Score Cards (Metrics) */
    [data-testid="stMetricValue"] {{
        font-size: 100px !important;
        font-weight: 800;
        color: #ffffff !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 45px !important;
        font-weight: 700;
        color: #FFD700 !important;
    }}

    .stMetric {{
        background: rgba(255, 255, 255, 0.12) !important;
        border: 3px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(15px);
        border-radius: 40px !important;
        padding: 40px !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.8);
    }}

    /* Table styling for Live Feed */
    .stTable {{ 
        font-size: 30px !important; 
        background-color: rgba(0,0,0,0.5) !important;
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
@st.cache_data(ttl=5) # 5 seconds delay refresh ekata
def get_live_data():
    try:
        # Source 1: Marks Entry Sheet eken data load karanawa
        df = pd.read_csv(MARKS_URL)
        return df
    except Exception as e:
        return None

df = get_live_data()

if df is not None:
    # Calculating Team-wise Total Scores
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)

    # --- TOP ROW: LIVE LEADERBOARD ---
    st.write("### 🏆 CURRENT STANDINGS")
    cols = st.columns(len(summary))
    for i, (idx, row) in enumerate(summary.iterrows()):
        with cols[i]:
            st.metric(label=row['Team '], value=int(row['Points Added']))

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MIDDLE SECTION: ADVANCED CHART & FEED ---
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.write("### 📊 LIVE PROGRESS CHART")
        # Horizontal Bar Chart එකක් දැම්මා TV එකේ ලස්සනට පේන්න
        fig = px.bar(
            summary, 
            y='Team ', 
            x='Points Added', 
            color='Team ', 
            orientation='h',
            text='Points Added',
            color_discrete_map={
                'Red': '#FF0000', 'Blue': '#0000FF', 
                'Green': '#008000', 'Yellow': '#FFFF00'
            }
        )
        
        # Chart UI Tweaks
        fig.update_layout(
            height=600,
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            font=dict(size=25, color="white"),
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, title="")
        )
        fig.update_traces(
            textfont_size=40, 
            textposition='outside',
            marker_line_color='white',
            marker_line_width=2,
            opacity=0.9
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("### 📢 RECENT UPDATES")
        # Latest entries showing at the top
        recent_activity = df.tail(6).iloc[::-1]
        st.table(recent_activity[['Team ', 'Points Added']])

else:
    st.error("Sheet data load karanna baha. Google Sheet eka public share karala thiyeda balanna.")

# 4. Auto-Refresh Logic (Every 10 seconds)
time.sleep(10)
st.rerun()
