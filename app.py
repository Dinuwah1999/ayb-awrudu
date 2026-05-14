import streamlit as st
import pandas as pd
import plotly.express as px
import time

# Page configuration
st.set_page_config(page_title="Ayathi Avurudu Udanaya Dashboard", layout="wide")

# Advanced CSS for Image-like UI
st.markdown("""
    <style>
    /* Dark Theme Background */
    .main { background-color: #0b0e14; color: #ffffff; }
    
    /* Title Styling */
    .main-title {
        font-size: 42px; font-weight: 800; text-align: center;
        background: -webkit-linear-gradient(#FFD700, #FFA500);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px;
    }

    /* Glassmorphism Card Effect */
    .stMetric, .card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Ranking Badge colors */
    .rank-1 { color: #FFD700; font-weight: bold; } /* Gold */
    .rank-2 { color: #C0C0C0; font-weight: bold; } /* Silver */
    .rank-3 { color: #CD7F32; font-weight: bold; } /* Bronze */

    /* Dataframe/Table customization */
    .stDataFrame { border-radius: 15px; overflow: hidden; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Ayathi Avurudu Udanaya 2026</h1>', unsafe_allow_html=True)

# Google Sheet Details
SHEET_ID = "1W7emxpy74FY1sCFqmuOt5zQP1bVrIJtekMqSYiFOEMQ"
# GID values update karanna (Marks: 0, Summary: check your browser URL gid)
MARKS_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=10) # 10 seconds cache to prevent heavy loading
def load_data(url):
    try:
        return pd.read_csv(url)
    except:
        return None

marks_df = load_data(MARKS_URL)

if marks_df is not None:
    # --- REAL-TIME CALCULATIONS ---
    # Team Summary eka live hadagamu (Marks entry ekenma)
    summary_df = marks_df.groupby('Team ').agg({'Points Added': 'sum'}).reset_index()
    summary_df.columns = ['Team Name', 'Total Score']
    summary_df = summary_df.sort_values(by='Total Score', ascending=False)
    summary_df['Ranking'] = range(1, len(summary_df) + 1)

    # --- TOP ROW: LEADERBOARD CARDS ---
    st.write("### 🏆 Top Standings")
    cols = st.columns(len(summary_df))
    
    for i, (idx, row) in enumerate(summary_df.iterrows()):
        with cols[i]:
            rank_class = f"rank-{row['Ranking']}" if row['Ranking'] <= 3 else ""
            st.metric(
                label=f"{row['Team Name']}", 
                value=f"{row['Total Score']} Pts",
                delta=f"Rank {row['Ranking']}"
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MIDDLE SECTION: LAYOUT LIKE YOUR IMAGE ---
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.write("### 📊 Performance Analysis")
        # Bar Chart with Custom Colors
        fig = px.bar(
            summary_df, x='Team Name', y='Total Score', 
            color='Team Name', text='Total Score',
            color_discrete_map={
                'Red': '#ff4b4b', 'Blue': '#0078ff', 
                'Green': '#28a745', 'Yellow': '#ffc107'
            },
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="", yaxis_title="Total Points"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.write("### ⚡ Live Feed")
        # Latest entries highlight wela ena widihata
        recent_marks = marks_df.tail(10).iloc[::-1]
        st.dataframe(
            recent_marks[['Time', 'Team ', 'Game Name', 'Points Added']], 
            hide_index=True, 
            use_container_width=True
        )

    # --- BOTTOM SECTION: DETAILED BREAKDOWN ---
    with st.expander("Detailed Points Table"):
        st.table(summary_df)

    # Footer update time
    st.markdown(f"<p style='text-align: center; color: gray;'>Last Updated: {time.strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)

else:
    st.error("Sheet data load karanna baha. Permissions check karanna.")

# Auto refresh set to 15 seconds
time.sleep(15)
st.rerun()
