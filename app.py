import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Page Configuration
st.set_page_config(page_title="Ayathi Avurudu Udanaya 2026", layout="wide")

# Custom CSS for "Supiri" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 20px; border-radius: 15px; border: 1px solid #3e4251; }
    .title-text { text-align: center; color: #FFD700; font-size: 45px; font-weight: bold; text-shadow: 2px 2px #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title-text">🎊 Ayathi Avurudu Udanaya 2026 Live Dashboard 🎊</p>', unsafe_allow_html=True)

# Google Sheet URLs (CSV format)
# GID 0 kiyanne godak welata 1st tab eka. Marks entry saha summary tabs wala GID wenas wenna puluwan.
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0" 
SUMMARY_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=123456789" # Summary tab eke GID eka methanata danna

def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return None

# Sidebar - Settings
st.sidebar.header("Settings")
refresh_rate = st.sidebar.slider("Auto Refresh (Seconds)", 5, 60, 10)

# Main Dashboard Logic
marks_df = load_data(MARKS_URL)
# Simulation ekak widiyata summary eka marks_df ekenma hadagamu sheet eke data update wenakan
if marks_df is not None:
    # Summary calculation (Real-time)
    summary_df = marks_df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary_df.columns = ['Team Name', 'Total Score']
    summary_df = summary_df.sort_values(by='Total Score', ascending=False)
    summary_df['Ranking'] = range(1, len(summary_df) + 1)

    # --- TOP ROW: LEADERBOARD ---
    st.subheader("🏆 Live Leaderboard")
    cols = st.columns(len(summary_df))
    for i, (idx, row) in enumerate(summary_df.iterrows()):
        with cols[i]:
            st.metric(label=f"Rank {row['Ranking']} - {row['Team Name']}", 
                      value=f"{row['Total Score']} Pts")

    st.markdown("---")

    # --- MIDDLE ROW: CHARTS ---
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.write("### 📊 Team Standings")
        fig = px.bar(summary_df, x='Team Name', y='Total Score', 
                     color='Team Name', text='Total Score',
                     color_discrete_map={'Red': '#FF4B4B', 'Blue': '#1F77B4', 'Green': '#2CA02C', 'Yellow': '#FFD700'})
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("### 🔔 Recent Updates")
        recent_marks = marks_df.tail(10).iloc[::-1]
        st.dataframe(recent_marks[['Time', 'Team ', 'Game Name', 'Points Added']], hide_index=True, use_container_width=True)

    # --- FOOTER ---
    st.info(f"Last updated: {time.strftime('%H:%M:%S')}. Next update in {refresh_rate}s.")

else:
    st.warning("⚠️ Data load karanna ba. Sheet permissions check karanna.")

# Auto-refresh logic
time.sleep(refresh_rate)
st.rerun()
