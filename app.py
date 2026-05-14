import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. Page Configuration
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026", layout="wide")

# --- SETTINGS ---
IMAGE_FILE_ID = "1fDnUlHbPnaRcJHsg_OvnVjEdkpCM2WCa"
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"
BG_URL = f"https://lh3.googleusercontent.com/u/0/d/{IMAGE_FILE_ID}"

# 2. Dynamic TV Scaling CSS
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("{BG_URL}");
        background-size: cover;
        background-position: center;
        height: 100vh;
        overflow: hidden;
    }}
    
    .block-container {{
        padding-top: 2vh !important;
        padding-bottom: 0 !important;
        max-width: 95% !important;
    }}

    .main-title {{
        font-size: 6vh !important; 
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        margin-top: -2vh;
        text-transform: uppercase;
        text-shadow: 3px 3px 15px black;
    }}

    .section-head {{
        font-size: 3vh !important;
        color: white;
        text-align: center;
        margin-top: 1vh;
        margin-bottom: 1vh;
    }}

    /* Progress Chart eka pahalata ganna aluth style eka */
    .chart-heading {{
        font-size: 3vh !important;
        color: white;
        text-align: center;
        margin-top: 10vh !important; /* Meken thama chart eka pahalata thallu karanne */
        margin-bottom: 1vh;
    }}

    .team-card {{
        padding: 2vh;
        border-radius: 2.5vh;
        text-align: center;
        border: 0.4vh solid;
        backdrop-filter: blur(10px);
    }}
    .red-card {{ background: rgba(255, 0, 0, 0.25); border-color: #FF0000; }}
    .blue-card {{ background: rgba(30, 144, 255, 0.25); border-color: #1E90FF; }}
    .green-card {{ background: rgba(50, 205, 50, 0.25); border-color: #32CD32; }}
    .yellow-card {{ background: rgba(255, 215, 0, 0.25); border-color: #FFD700; }}

    .card-label {{ font-size: 2.5vh !important; font-weight: bold; margin: 0; }}
    .card-points {{ font-size: 8vh !important; font-weight: 800; margin: 0; line-height: 1; }}

    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data(ttl=5)
def get_live_data():
    try:
        data = pd.read_csv(MARKS_URL)
        data.columns = data.columns.str.strip()
        return data
    except:
        return None

df = get_live_data()

if df is not None:
    summary = df.groupby('Team').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)
    
    colors_map = {'Red': '#FF0000', 'Blue': '#1E90FF', 'Green': '#32CD32', 'Yellow': '#FFD700'}
    class_map = {'Red': 'red-card', 'Blue': 'blue-card', 'Green': 'green-card', 'Yellow': 'yellow-card'}

    # --- 🥇 LIVE STANDINGS ---
    st.markdown('<p class="section-head">🥇 LIVE STANDINGS</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (idx, row) in enumerate(summary.iterrows()):
        t_name = row['Team'].strip()
        t_points = int(row['Points Added'])
        with cols[i]:
            st.markdown(f"""
                <div class="team-card {class_map.get(t_name, '')}">
                    <p class="card-label" style="color: {colors_map.get(t_name)};">{t_name}</p>
                    <p class="card-points" style="color: white;">{t_points}</p>
                </div>
                """, unsafe_allow_html=True)

    # --- 📊 PROGRESS CHART ---
    # Aluth style eka methana apply kara
    st.markdown('<p class="chart-heading">📊 POINTS PROGRESS</p>', unsafe_allow_html=True)
    
    fig = px.bar(summary, y='Team', x='Points Added', color='Team', 
                 text='Points Added', orientation='h', color_discrete_map=colors_map)
    
    fig.update_layout(
        height=350, # Pahalata thallu karapu nisa height eka poddak balance kala
        margin=dict(l=20, r=60, t=10, b=10),
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(size=18, color="white"),
        showlegend=False,
        xaxis=dict(visible=False),
        yaxis=dict(title="", tickfont=dict(size=25, color="white"))
    )
    fig.update_traces(textfont_size=30, textposition='outside', cliponaxis=False)
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

else:
    st.error("Google Sheet Connect Wenne Na!")

# Refresh
time.sleep(10)
st.rerun()
