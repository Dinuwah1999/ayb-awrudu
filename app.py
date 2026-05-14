import streamlit as st
import pandas as pd
import plotly.express as px
import time
import base64

# Page configuration for TV (Wide mode)
st.set_page_config(page_title="Ayathi Avurudu Udanaya - TV", layout="wide")

# --- BACKGROUND IMAGE SETTING ---
# Oyaage image eka "background.jpg" kiyala repo ekata danna. 
# Nathnam online link ekak danna puluwan.
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Adding a dark overlay to make text readable */
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.6); /* 60% black overlay */
        z-index: -1;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Meeka run karanna kalin image ekak repo ekata danna (Ex: bg.png)
# set_background('bg.png') 

# --- ADVANCED CSS FOR TV DISPLAY ---
st.markdown("""
    <style>
    /* TV optimized Big Fonts */
    html, body, [class*="st-"] {
        font-family: 'Arial Black', Gadget, sans-serif;
    }
    
    .main-title {
        font-size: 70px !important; /* Huge title for TV */
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 4px 4px 10px rgba(0,0,0,0.8);
        margin-bottom: 50px;
    }

    /* Big Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 60px !important; /* Large numbers */
        font-weight: bold;
        color: #ffffff;
    }
    [data-testid="stMetricLabel"] {
        font-size: 30px !important; /* Large team names */
        color: #FFD700;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
        padding: 30px !important;
        border-radius: 25px !important;
    }

    /* Hide Streamlit elements for clean TV look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# Google Sheet Data Load
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

def load_data():
    try:
        df = pd.read_csv(MARKS_URL)
        return df
    except:
        return None

marks_df = load_data()

if marks_df is not None:
    # Live Summary
    summary_df = marks_df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary_df.columns = ['Team Name', 'Total Score']
    summary_df = summary_df.sort_values(by='Total Score', ascending=False)
    
    # --- LEADERBOARD (FULL WIDTH CARDS) ---
    st.write("### 🏆 LEADERBOARD")
    cols = st.columns(len(summary_df))
    for i, (idx, row) in enumerate(summary_df.iterrows()):
        with cols[i]:
            st.metric(label=row['Team Name'], value=int(row['Total Score']))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- CHARTS SECTION ---
    col_chart, col_feed = st.columns([2, 1])

    with col_chart:
        fig = px.bar(
            summary_df, x='Team Name', y='Total Score', 
            color='Team Name', text='Total Score',
            color_discrete_map={
                'Red': '#FF0000', 'Blue': '#0000FF', 
                'Green': '#008000', 'Yellow': '#FFFF00'
            }
        )
        fig.update_traces(textfont_size=25, textposition='outside')
        fig.update_layout(
            height=600,
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=20, color="white"),
            xaxis={'categoryorder':'total descending'}
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_feed:
        st.write("### 🔔 LATEST SCORES")
        recent = marks_df.tail(6).iloc[::-1]
        # Custom Table Styling for TV
        st.table(recent[['Team ', 'Points Added']])

else:
    st.error("Data load kireeme doshayaki!")

# Auto Refresh for Live TV Feel (Every 10 seconds)
time.sleep(10)
st.rerun()
