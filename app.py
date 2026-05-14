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

# 2. Advanced CSS for Color-Coded Metrics & Horizontal Chart
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
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 5px;
    }}

    /* Global Metric Tweaks */
    [data-testid="stMetricValue"] {{ font-size: 90px !important; font-weight: 800; color: white !important; }}
    [data-testid="stMetricLabel"] {{ font-size: 40px !important; font-weight: 700; color: white !important; }}

    /* Custom Color Cards Classes */
    .team-card {{
        padding: 30px;
        border-radius: 35px;
        text-align: center;
        border: 4px solid;
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }}
    .red-card {{ background: rgba(255, 0, 0, 0.25); border-color: #FF0000; }}
    .blue-card {{ background: rgba(30, 144, 255, 0.25); border-color: #1E90FF; }}
    .green-card {{ background: rgba(50, 205, 50, 0.25); border-color: #32CD32; }}
    .yellow-card {{ background: rgba(255, 215, 0, 0.25); border-color: #FFD700; }}

    .stTable {{ font-size: 26px !important; color: white !important; }}
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
    # Calculations
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)
    
    # Team color mapping
    colors_map = {'Red': '#FF0000', 'Blue': '#1E90FF', 'Green': '#32CD32', 'Yellow': '#FFD700'}
    class_map = {'Red': 'red-card', 'Blue': 'blue-card', 'Green': 'green-card', 'Yellow': 'yellow-card'}

    # --- TOP: COLOR CODED CARDS ---
    st.markdown("<h2 style='text-align: center; color: white; font-size: 35px;'>🏆 LIVE STANDINGS</h2>", unsafe_allow_html=True)
    cols = st.columns(len(summary))
    
    for i, (idx, row) in enumerate(summary.iterrows()):
        t_name = row['Team '].strip()
        t_points = int(row['Points Added'])
        t_class = class_map.get(t_name, "")
        t_color = colors_map.get(t_name, "#FFFFFF")
        
        with cols[i]:
            st.markdown(f"""
                <div class="team-card {t_class}">
                    <p style='font-size: 35px; font-weight: bold; margin: 0; color: {t_color};'>{t_name}</p>
                    <p style='font-size: 80px; font-weight: 800; margin: 0; color: white;'>{t_points}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MIDDLE: HORIZONTAL PROGRESS CHART ---
    st.markdown("<h2 style='text-align: center; color: white; font-size: 35px;'>📊 POINTS PROGRESS</h2>", unsafe_allow_html=True)
    fig = px.bar(
        summary, y='Team ', x='Points Added', color='Team ', 
        text='Points Added', orientation='h',
        color_discrete_map=colors_map
    )
    fig.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(size=22, color="white"),
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(title="", tickfont=dict(size=30, color="white"))
    )
    fig.update_traces(
        textfont_size=40, textposition='outside',
        marker_line_color='white', marker_line_width=2
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- BOTTOM: LATEST UPDATES ---
    st.markdown("<h3 style='text-align: center; color: #FFD700;'>🔔 LATEST UPDATES</h3>", unsafe_allow_html=True)
    recent_activity = df.tail(4).iloc[::-1]
    st.table(recent_activity[['Team ', 'Game Name', 'Points Added']])

else:
    st.error("Data loading issue!")

# Auto-Refresh
time.sleep(10)
st.rerun()
