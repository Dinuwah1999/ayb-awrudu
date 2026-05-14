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

# 2. Optimized CSS for Side-by-Side View
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
                    url("{BG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }}

    .main-title {{
        font-size: 3.2vw !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 3px 3px 12px rgba(0,0,0,1);
        margin-top: -50px;
        text-transform: uppercase;
    }}

    .team-card {{
        padding: 10px;
        border-radius: 20px;
        text-align: center;
        border: 3px solid;
        backdrop-filter: blur(8px);
    }}
    .red-card {{ background: rgba(255, 0, 0, 0.25); border-color: #FF0000; }}
    .blue-card {{ background: rgba(30, 144, 255, 0.25); border-color: #1E90FF; }}
    .green-card {{ background: rgba(50, 205, 50, 0.25); border-color: #32CD32; }}
    .yellow-card {{ background: rgba(255, 215, 0, 0.25); border-color: #FFD700; }}

    .stTable {{ font-size: 1.1vw !important; color: white !important; }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data(ttl=3)
def get_live_data():
    try:
        data = pd.read_csv(MARKS_URL)
        data.columns = data.columns.str.strip() # Column names wala spaces ain karanawa
        return data
    except:
        return None

df = get_live_data()

if df is not None:
    summary = df.groupby('Team').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)
    
    colors_map = {'Red': '#FF0000', 'Blue': '#1E90FF', 'Green': '#32CD32', 'Yellow': '#FFD700'}
    class_map = {'Red': 'red-card', 'Blue': 'blue-card', 'Green': 'green-card', 'Yellow': 'yellow-card'}

    # --- TOP: STANDINGS ---
    cols = st.columns(len(summary))
    for i, (idx, row) in enumerate(summary.iterrows()):
        t_name = row['Team'].strip()
        t_points = int(row['Points Added'])
        t_class = class_map.get(t_name, "")
        t_color = colors_map.get(t_name, "#FFFFFF")
        with cols[i]:
            st.markdown(f"""<div class="team-card {t_class}">
                <p style='font-size: 1.3vw; font-weight: bold; margin: 0; color: {t_color};'>{t_name}</p>
                <p style='font-size: 3.5vw; font-weight: 800; margin: 0; color: white;'>{t_points}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MAIN CONTENT: Side-by-Side ---
    left_col, right_col = st.columns([1.3, 1])

    with left_col:
        st.markdown("<p style='color: white; font-size: 1.8vw; font-weight: bold; text-align: center;'>📊 POINTS PROGRESS</p>", unsafe_allow_html=True)
        fig = px.bar(summary, y='Team', x='Points Added', color='Team', 
                     text='Points Added', orientation='h', color_discrete_map=colors_map)
        fig.update_layout(height=380, margin=dict(l=10, r=40, t=10, b=10),
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          font=dict(size=14, color="white"), showlegend=False,
                          xaxis=dict(visible=False), yaxis=dict(title="", tickfont=dict(size=22, color="white")))
        fig.update_traces(textfont_size=25, textposition='outside', cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with right_col:
        st.markdown("<p style='color: #FFD700; font-size: 1.8vw; font-weight: bold; text-align: center;'>🔔 LATEST UPDATES</p>", unsafe_allow_html=True)
        if not df.empty:
            # Column names sheet eke thiyena widiyatama methana danna
            # "Team", "Game Name", "Points Added"
            recent = df.tail(6).iloc[::-1]
            st.table(recent[['Team', 'Game Name', 'Points Added']])

else:
    st.error("Data Load Wenne Na! Google Sheet link eka check karanna.")

# Refresh
time.sleep(10)
st.rerun()
