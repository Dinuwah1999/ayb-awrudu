import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. Page Configuration
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026 - Live", layout="wide")

# --- SETTINGS ---
IMAGE_FILE_ID = "1fDnUlHbPnaRcJHsg_OvnVjEdkpCM2WCa"
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
BG_URL = f"https://lh3.googleusercontent.com/u/0/d/{IMAGE_FILE_ID}"

# 2. TV-Optimized Layout Fix
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Header Fixed - Screen ekata fit wenna */
    .main-title {{
        font-size: 3.5vw !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 3px 3px 10px rgba(0,0,0,1);
        margin-top: -80px; /* Aligned for TV top */
        padding-bottom: 10px;
        text-transform: uppercase;
    }}

    /* Team Cards */
    .team-card {{
        padding: 1vw;
        border-radius: 20px;
        text-align: center;
        border: 3px solid;
        backdrop-filter: blur(8px);
    }}
    .red-card {{ background: rgba(255, 0, 0, 0.2); border-color: #FF0000; }}
    .blue-card {{ background: rgba(30, 144, 255, 0.2); border-color: #1E90FF; }}
    .green-card {{ background: rgba(50, 205, 50, 0.2); border-color: #32CD32; }}
    .yellow-card {{ background: rgba(255, 215, 0, 0.2); border-color: #FFD700; }}

    /* Table Compact Styling */
    div[data-testid="stTable"] {{
        background: rgba(0,0,0,0.4);
        border-radius: 15px;
        font-size: 1.5vw !important;
    }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# Title Highlight
st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data(ttl=3)
def get_live_data():
    try:
        data = pd.read_csv(MARKS_URL)
        return data
    except:
        return None

df = get_live_data()

if df is not None:
    # Calculations
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)
    
    colors_map = {'Red': '#FF0000', 'Blue': '#1E90FF', 'Green': '#32CD32', 'Yellow': '#FFD700'}
    class_map = {'Red': 'red-card', 'Blue': 'blue-card', 'Green': 'green-card', 'Yellow': 'yellow-card'}

    # --- TOP: COLOR CODED CARDS ---
    cols = st.columns(len(summary))
    for i, (idx, row) in enumerate(summary.iterrows()):
        t_name = row['Team '].strip()
        t_points = int(row['Points Added'])
        t_class = class_map.get(t_name, "")
        t_color = colors_map.get(t_name, "#FFFFFF")
        
        with cols[i]:
            st.markdown(f"""
                <div class="team-card {t_class}">
                    <p style='font-size: 1.8vw; font-weight: bold; margin: 0; color: {t_color};'>{t_name}</p>
                    <p style='font-size: 4vw; font-weight: 800; margin: 0; color: white;'>{t_points}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- MIDDLE: PROGRESS CHART (Dynamic Height) ---
    fig = px.bar(
        summary, y='Team ', x='Points Added', color='Team ', 
        text='Points Added', orientation='h',
        color_discrete_map=colors_map
    )
    fig.update_layout(
        height=300, # Fixed low height for TV fit
        margin=dict(l=10, r=40, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(size=18, color="white"), 
        showlegend=False,
        xaxis=dict(visible=False), 
        yaxis=dict(title="", tickfont=dict(size=22, color="white"))
    )
    fig.update_traces(textfont_size=28, textposition='outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- BOTTOM: LATEST UPDATES (Heading visible) ---
    st.markdown("<p style='text-align: center; color: #FFD700; font-size: 2.2vw; font-weight: bold; margin-top: -10px;'>🔔 LATEST SCORE UPDATES</p>", unsafe_allow_html=True)
    
    # Table eke rows 3kata fix kara TV eke yata penna ona nisa
    recent_activity = df.tail(3).iloc[::-1]
    st.table(recent_activity[['Team ', 'Game Name', 'Points Added']])

else:
    st.warning("🔄 Connecting to Google Sheets...")

# Refresh
time.sleep(10)
st.rerun()
