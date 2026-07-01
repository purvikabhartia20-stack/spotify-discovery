import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Base styles */
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            color: #ffffff;
            background-color: #121212;
        }
        
        /* Spotify Green accents */
        :root {
            --primary-color: #1DB954;
            --background-color: #121212;
            --secondary-background-color: #181818;
            --text-color: #ffffff;
            --secondary-text: #b3b3b3;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #1DB954 !important;
            color: black !important;
            border-radius: 20px !important;
            border: none !important;
            padding: 10px 24px !important;
            font-weight: bold !important;
            transition: all 0.2s ease;
        }
        
        .stButton>button:hover {
            transform: scale(1.04);
            background-color: #1ed760 !important;
        }
        
        /* Metric cards */
        div[data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 900 !important;
            color: #1DB954 !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding-top: 16px;
            padding-bottom: 16px;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #000000;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background-color: #1DB954;
        }
        
        /* Cards container */
        .metric-card {
            background: rgba(24, 24, 24, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 24px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 16px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(29, 185, 84, 0.1);
            border: 1px solid rgba(29, 185, 84, 0.3);
        }
        
        .metric-title {
            color: var(--secondary-text);
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }
        
        .metric-value {
            color: var(--primary-color);
            font-size: 2.2rem;
            font-weight: 900;
            margin: 0;
            line-height: 1.2;
        }
        
        /* Table enhancements */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        </style>
    """, unsafe_allow_html=True)
