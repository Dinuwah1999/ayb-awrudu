import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 1. Page Config
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026", layout="wide")

# 2. Advanced CSS with Fixed Background Logic
# Note: 'image_b10cfb.jpg' kiyana file eka oyaage GitHub repo eke thiyenna ona.
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url("https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/image_b10cfb.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Title for TV */
    .main-title {{
        font-size: 85px !important;
        font-weight: 900;
        text-align: center;
        color: #FFD700;
        text-shadow: 4px 4px 15px rgba(0,0,0,0.9);
        padding-top: 20px;
        margin-bottom: 40px;
        text-transform: uppercase;
    }}

    /* Huge Metrics for TV */
    [data-testid="stMetricValue"] {{
        font-size: 90px !important;
        font-weight: 800;
        color: #ffffff !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 40px !important;
        font-weight: 600;
        color: #FFD700 !important;
    }}

    .stMetric {{
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(15px);
        border-radius: 30px !important;
        padding: 35px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    /* Table styling */
    .stTable {{
        background: rgba(0, 0, 0, 0.5);
        border-radius: 20px;
    }}
    
    /* Hide Streamlit components */
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">AYATHI AVRUDU UDANAYA 2026</p>', unsafe_allow_html=True)

# 3. Data Fetching (Using Source [cite: 1])
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

def get_data():
    try:
        # Fetching directly from Google Sheets
        return pd.read_csv(MARKS_URL)
    except:
        return None

df = get_data()

if df is not None:
    # Calculating scores [cite: 1]
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary = summary.sort_values(by='Points Added', ascending=False)

    # Leaderboard row
    st.write("### 🥇 TOP STANDINGS")
    cols = st.columns(len(summary))
    for i, (idx, row) in enumerate(summary.iterrows()):
        with cols[i]:
            st.metric(label=row['Team '], value=int(row['Points Added']))

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Middle Content: Chart & Feed
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.write("### 📊 LIVE CHART")
        fig = px.bar(summary, x='Team ', y='Points Added', color='Team ', 
                     text='Points Added',
                     color_discrete_map={'Red':'#FF0000', 'Blue':'#0000FF', 
                                         'Green':'#008000', 'Yellow':'#FFFF00'})
        fig.update_layout(height=550, plot_bgcolor='rgba(0,0,0,0)', 
                          paper_bgcolor='rgba(0,0,0,0)', 
                          font=dict(size=22, color="white"))
        fig.update_traces(textfont_size=35, textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.write("### 🔔 RECENT UPDATES")
        # Showing latest 5 entries [cite: 1]
        st.table(df.tail(6)[['Team ', 'Game Name', 'Points Added']].iloc[::-1])

# Auto Refresh 10s
time.sleep(10)
st.rerun()
