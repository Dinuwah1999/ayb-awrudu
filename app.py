import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Page Configuration for TV
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026", layout="wide")

# --- ULTIMATE CSS FOR TV & BACKGROUND ---
st.markdown("""
    <style>
    /* Background Image from Web (Dark & Professional) */
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1550684848-fac1c5b4e853?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Overlay to make content pop */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.7);
        z-index: -1;
    }

    /* Title Styling */
    .main-title {
        font-size: 80px !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(to right, #FFD700, #FFA500, #FF4500);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 20px rgba(0,0,0,0.5);
        margin-bottom: 40px;
        font-family: 'Arial Black';
    }

    /* Glassmorphism Leaderboard Cards */
    .leaderboard-card {
        background: rgba(255, 255, 255, 0.08);
        border: 2px solid rgba(255, 255, 255, 0.15);
        padding: 30px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        margin: 10px;
    }

    .team-name { font-size: 35px; font-weight: bold; color: #FFD700; margin-bottom: 10px; }
    .team-score { font-size: 65px; font-weight: 900; color: #ffffff; }
    .team-rank { font-size: 25px; color: #00FFCC; font-style: italic; }

    /* Custom Table for TV */
    .stTable { background: rgba(0,0,0,0.4); border-radius: 20px; font-size: 24px; }
    
    /* Remove default Streamlit clutter */
    header, footer, #MainMenu { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">AYATHI AVRUDU UDANAYA 2026</h1>', unsafe_allow_html=True)

# Google Sheet URL
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=5)
def load_data():
    try:
        return pd.read_csv(MARKS_URL)
    except:
        return None

df = load_data()

if df is not None:
    # 1. Real-time Summary
    summary = df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary.columns = ['Team Name', 'Total Score']
    summary = summary.sort_values(by='Total Score', ascending=False)
    summary['Rank'] = range(1, len(summary) + 1)

    # 2. Leaderboard Grid (Mulu dashboard ekama wenas kara)
    st.markdown("### 🥇 LEADERBOARD")
    cols = st.columns(len(summary))
    
    for i, (idx, row) in enumerate(summary.iterrows()):
        with cols[i]:
            st.markdown(f"""
                <div class="leaderboard-card">
                    <div class="team-rank"># {row['Rank']}</div>
                    <div class="team-name">{row['Team Name']}</div>
                    <div class="team-score">{int(row['Total Score'])}</div>
                    <div style="color: gray;">POINTS</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 3. Chart & Feed Section
    col_chart, col_feed = st.columns([1.8, 1.2])

    with col_chart:
        st.write("### 📈 SCORE PROGRESSION")
        # Horizontal Chart for better TV fit
        fig = px.bar(
            summary, y='Team Name', x='Total Score', 
            orientation='h',
            color='Team Name', text='Total Score',
            color_discrete_map={'Red': '#FF3131', 'Blue': '#007FFF', 'Green': '#39FF14', 'Yellow': '#FFFF33'}
        )
        fig.update_traces(textfont_size=30, textposition='inside')
        fig.update_layout(
            height=500,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=22, color="white"),
            xaxis=dict(showgrid=False, title=""),
            yaxis=dict(showgrid=False, title="", tickfont=dict(size=25))
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_feed:
        st.write("### 🔔 LIVE UPDATES")
        recent = df.tail(8).iloc[::-1]
        # Professional dark dataframe
        st.dataframe(
            recent[['Team ', 'Game Name', 'Points Added']], 
            use_container_width=True, 
            hide_index=True
        )

    st.markdown(f"<p style='text-align: right; color: #444;'>Refresh Cycle: 5s | {time.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

else:
    st.error("Sheet eka connect kireeme doshayaki. Permissions check karanna.")

# Auto Refresh (Fast 5 seconds for TV)
time.sleep(5)
st.rerun()
