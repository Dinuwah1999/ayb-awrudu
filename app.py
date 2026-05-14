import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. Page Configuration
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026 - Live", layout="wide")

# --- SETTINGS ---
# Background image eka oyaage GitHub eke thiyena widiyata local file ekak gannawa
BG_IMAGE = "background.jpg" 
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# 2. CSS for Vertical List Layout
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                    url("https://raw.githubusercontent.com/Dinuwah1999/ayb-awrudu/main/background.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; }}

    .main-title {{
        font-size: 3.5vw !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 3px 3px 15px rgba(0,0,0,1);
        margin-top: -30px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }}

    /* Team Cards Styling */
    .team-card {{
        padding: 12px;
        border-radius: 20px;
        text-align: center;
        border: 4px solid;
        backdrop-filter: blur(10px);
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }}
    .red-card {{ background: rgba(255, 0, 0, 0.3); border-color: #FF0000; }}
    .blue-card {{ background: rgba(30, 144, 255, 0.3); border-color: #1E90FF; }}
    .green-card {{ background: rgba(50, 205, 50, 0.3); border-color: #32CD32; }}
    .yellow-card {{ background: rgba(255, 215, 0, 0.3); border-color: #FFD700; }}

    /* Highlight Section for Latest Updates */
    .update-container {{
        background: rgba(0, 0, 0, 0.6);
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 15px;
        margin-top: 15px;
    }}

    .stTable {{
        font-size: 1.4vw !important;
        color: white !important;
    }}
    
    /* Highlight the very first row of the table */
    .stTable tr:first-child {{
        background-color: rgba(255, 215, 0, 0.4) !important;
        color: #FFD700 !important;
        font-weight: bold;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data(ttl=2)
def get_live_data():
    try:
        data = pd.read_csv(MARKS_URL)
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = get_live_data()

if df is not None:
    # Calculations
    summary = df.groupby('Team').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)
    
    colors_map = {'Red': '#FF0000', 'Blue': '#1E90FF', 'Green': '#32CD32', 'Yellow': '#FFD700'}
    class_map = {'Red': 'red-card', 'Blue': 'blue-card', 'Green': 'green-card', 'Yellow': 'yellow-card'}

    # --- 1. TOP STANDINGS ---
    cols = st.columns(4)
    for i, (idx, row) in enumerate(summary.iterrows()):
        t_name = row['Team']
        t_points = int(row['Points Added'])
        with cols[i]:
            st.markdown(f"""<div class="team-card {class_map.get(t_name, '')}">
                <p style='font-size: 1.5vw; font-weight: bold; margin: 0; color: {colors_map.get(t_name, '#FFF')};'>{t_name}</p>
                <p style='font-size: 4vw; font-weight: 800; margin: 0; color: white;'>{t_points}</p>
            </div>""", unsafe_allow_html=True)

    # --- 2. POINTS PROGRESS (CHART) ---
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: white; font-size: 1.8vw; font-weight: bold; margin: 0;'>📊 POINTS PROGRESS</p>", unsafe_allow_html=True)
    
    fig = px.bar(summary, y='Team', x='Points Added', color='Team', 
                 text='Points Added', orientation='h', color_discrete_map=colors_map)
    fig.update_layout(height=280, margin=dict(l=20, r=50, t=10, b=10),
                      plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                      font=dict(size=14, color="white"), showlegend=False,
                      xaxis=dict(visible=False), yaxis=dict(title="", tickfont=dict(size=22, color="white")))
    fig.update_traces(textfont_size=26, textposition='outside', cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- 3. LATEST SCORE UPDATES ---
    st.markdown('<div class="update-container">', unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFD700; font-size: 1.8vw; font-weight: bold; margin-bottom: 10px;'>🔔 LATEST SCORE UPDATES</p>", unsafe_allow_html=True)
    
    # Anthima updates 5ka table ekak widiyata
    if not df.empty:
        recent = df.tail(5).iloc[::-1]
        st.table(recent[['Team', 'Game Name', 'Points Added']])
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("Google Sheet ekata data load wenne na mchn. Connection balanna.")

# Refresh Rate
time.sleep(10)
st.rerun()
