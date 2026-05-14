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

# 2. CSS for TV Layout
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
        font-size: 70px !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 4px 4px 15px rgba(0,0,0,1);
        margin-bottom: 20px;
        text-transform: uppercase;
    }}

    /* Custom Color Cards */
    .team-card {{
        padding: 20px;
        border-radius: 30px;
        text-align: center;
        border: 4px solid;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .red-card {{ background: rgba(255, 0, 0, 0.2); border-color: #FF0000; }}
    .blue-card {{ background: rgba(30, 144, 255, 0.2); border-color: #1E90FF; }}
    .green-card {{ background: rgba(50, 205, 50, 0.2); border-color: #32CD32; }}
    .yellow-card {{ background: rgba(255, 215, 0, 0.2); border-color: #FFD700; }}

    /* Table Styling */
    .stTable {{ 
        font-size: 24px !important; 
        color: white !important;
        background: rgba(0,0,0,0.4) !important;
        border-radius: 20px;
    }}
    
    /* Hide Default UI */
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
    
    colors_map = {'Red': '#FF0000', 'Blue': '#1E90FF', 'Green': '#32CD32', 'Yellow': '#FFD700'}
    class_map = {'Red': 'red-card', 'Blue': 'blue-card', 'Green': 'green-card', 'Yellow': 'yellow-card'}

    # --- TOP: COLOR CODED CARDS (Double points ain kala) ---
    cols = st.columns(len(summary))
    for i, (idx, row) in enumerate(summary.iterrows()):
        t_name = row['Team '].strip()
        t_points = int(row['Points Added'])
        t_class = class_map.get(t_name, "")
        t_color = colors_map.get(t_name, "#FFFFFF")
        
        with cols[i]:
            st.markdown(f"""
                <div class="team-card {t_class}">
                    <p style='font-size: 30px; font-weight: bold; margin: 0; color: {t_color};'>{t_name}</p>
                    <p style='font-size: 70px; font-weight: 800; margin: 0; color: white;'>{t_points}</p>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MIDDLE: HORIZONTAL CHART ---
    fig = px.bar(
        summary, y='Team ', x='Points Added', color='Team ', 
        text='Points Added', orientation='h',
        color_discrete_map=colors_map
    )
    fig.update_layout(
        height=380, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(size=20, color="white"), showlegend=False,
        xaxis=dict(visible=False), yaxis=dict(title="", tickfont=dict(size=25, color="white"))
    )
    fig.update_traces(textfont_size=35, textposition='outside', marker_line_color='white', marker_line_width=2)
    st.plotly_chart(fig, use_container_width=True)

    # --- BOTTOM: LATEST UPDATES (Dan lassanata penawa) ---
    st.markdown("<p style='text-align: center; color: #FFD700; font-size: 30px; font-weight: bold; margin-bottom: 5px;'>🔔 LATEST SCORE UPDATES</p>", unsafe_allow_html=True)
    recent_activity = df.tail(4).iloc[::-1] # Anthima update 4k
    st.table(recent_activity[['Team ', 'Game Name', 'Points Added']])

else:
    st.error("Sheet eka load wenne na mchn!")

# Refresh
time.sleep(10)
st.rerun()
