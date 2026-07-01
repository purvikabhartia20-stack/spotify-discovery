import streamlit as st
import os
import sys
import glob
import sqlite3
import pandas as pd
import subprocess
import time

from ui.styles import apply_custom_styles
from ui.charts import plot_theme_breakdown, get_recent_high_severity, plot_review_volume_over_time, plot_severity_by_theme, plot_reviews_by_source, get_platform_country_distribution
from ui.qa import stream_answer
from agents.export_pdf import export_report_to_pdf

# Force Streamlit to pick up changes in ui/charts.py!
st.set_page_config(page_title="Spotify Discovery Engine", page_icon="🎧", layout="wide")
apply_custom_styles()

def get_db_conn():
    return sqlite3.connect('data/reviews.db')

def fetch_metrics():
    conn = get_db_conn()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM reviews")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE tagged_at IS NOT NULL")
        tagged = cursor.fetchone()[0]
        
        cursor.execute("SELECT MAX(end_time), SUM(new_reviews_count) FROM runs")
        run_data = cursor.fetchone()
        last_refresh = run_data[0] if run_data[0] else "Never"
        new_since = run_data[1] if run_data[1] else 0
        
        # New Metrics
        cursor.execute("SELECT AVG(pain_severity) FROM reviews WHERE tagged_at IS NOT NULL AND pain_severity > 0")
        avg_sev = cursor.fetchone()[0]
        avg_sev = round(avg_sev, 1) if avg_sev else 0.0
        
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE tagged_at IS NOT NULL AND pain_severity >= 4")
        high_sev_count = cursor.fetchone()[0]
        high_sev_pct = round((high_sev_count / tagged * 100) if tagged > 0 else 0)
        
        cursor.execute("SELECT source FROM reviews GROUP BY source ORDER BY COUNT(*) DESC LIMIT 1")
        top_src = cursor.fetchone()
        top_source = top_src[0].title() if top_src else "None"
        
        cursor.execute("SELECT AVG(rating) FROM reviews WHERE rating IS NOT NULL")
        avg_rat = cursor.fetchone()[0]
        avg_rating = round(avg_rat, 1) if avg_rat else 0.0
        
    except:
        total = 0
        last_refresh = "Never"
        new_since = 0
        avg_sev = 0.0
        high_sev_pct = 0
        top_source = "None"
        avg_rating = 0.0
        
    conn.close()
    return total, new_since, last_refresh, avg_sev, high_sev_pct, top_source, avg_rating

# Header
st.title("🎧 Spotify Discovery Engine")
st.markdown("Analyze thousands of user reviews to solve music discovery.")

import datetime

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "🔄 Refresh Data", "📄 Insights Report", "💬 Ask Q&A", "📤 Upload Social Data"])

# ==========================================
# TAB 1: DASHBOARD
# ==========================================
with tab1:
    total, new_since, last_refresh, avg_sev, high_sev_pct, top_source, avg_rating = fetch_metrics()
    
    st.markdown("### Key Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Total Reviews</div>
            <div class="metric-value">{total:,}</div>
            <div style="color: #b3b3b3; font-size: 0.8rem; margin-top: 4px;">+{new_since} since last run</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">App Rating</div>
            <div class="metric-value" style="color: #ffc107;">{avg_rating} <span style="font-size: 1rem; color: #b3b3b3;">★</span></div>
            <div style="color: #b3b3b3; font-size: 0.8rem; margin-top: 4px;">Average store rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Discovery Insights")
    colA, colB = st.columns(2)
    with colA:
        fig_theme = plot_theme_breakdown()
        if fig_theme:
            st.plotly_chart(fig_theme, use_container_width=True)
            
        fig_src = plot_reviews_by_source()
        if fig_src:
            st.plotly_chart(fig_src, use_container_width=True)
            
    with colB:
        st.markdown("<br><b>Top Pain Points (High Severity)</b>", unsafe_allow_html=True)
        df_severe = get_recent_high_severity()
        if not df_severe.empty:
            st.dataframe(df_severe, use_container_width=True, hide_index=True)
        else:
            st.info("No high severity items found.")
            
        st.markdown("<br><b>Platform by Country Distribution</b>", unsafe_allow_html=True)
        df_dist = get_platform_country_distribution()
        if not df_dist.empty:
            st.dataframe(df_dist, use_container_width=True, hide_index=True)
        else:
            st.info("No distribution data found.")
            
    st.markdown("---")
    st.markdown("### Deep Dive: Review Explorer")
    st.markdown("Browse raw reviews and their AI-generated summaries. Filter by source to see data from Reddit, Apple, and more.")
    
    conn = get_db_conn()
    df_sources = pd.read_sql_query("SELECT DISTINCT source FROM reviews", conn)
    df_themes = pd.read_sql_query("SELECT DISTINCT theme FROM reviews WHERE theme IS NOT NULL", conn)
    
    source_list = ["All Sources"] + df_sources['source'].tolist()
    theme_list = df_themes['theme'].tolist()
    
    col_filt1, col_filt2 = st.columns(2)
    with col_filt1:
        selected_source = st.selectbox("Filter by Source", source_list)
    with col_filt2:
        selected_theme = st.multiselect("Filter by Theme", theme_list, placeholder="Select themes...")
    
    query = "SELECT date, source, theme, summary, text FROM reviews WHERE 1=1"
    if selected_source != "All Sources":
        query += f" AND source = '{selected_source}'"
    if selected_theme:
        themes_str = "','".join(selected_theme)
        query += f" AND theme IN ('{themes_str}')"
        
    query += " ORDER BY date DESC LIMIT 100"
    
    df_deepdive = pd.read_sql_query(query, conn)
        
    conn.close()
    
    if not df_deepdive.empty:
        st.dataframe(df_deepdive, use_container_width=True, hide_index=True)
    else:
        st.info("No reviews found.")

# ==========================================
# TAB 2: REFRESH DATA
# ==========================================
with tab2:
    st.header("Refresh Data Pipeline")
    st.markdown("Click below to pull the latest reviews from App Store, Play Store, Reddit, YouTube, and Social Media. It will automatically tag them and regenerate the Insights Report.")
    
    if st.button("🚀 Refresh All Data", use_container_width=True):
        if os.path.exists('pipeline.lock'):
            st.warning("Pipeline is already running! Please wait for it to finish.")
        else:
            st.markdown("### Pipeline Progress")
            
            with st.status("Running master pipeline...", expanded=True) as status:
                process = subprocess.Popen([sys.executable, "pipeline.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True, env={**os.environ, "PYTHONUTF8": "1"})
                
                output_container = st.empty()
                log_text = ""
                for line in process.stdout:
                    log_text += line
                    output_container.text(log_text)
                    
                process.wait()
                
                if process.returncode == 0:
                    status.update(label="✅ Refresh Complete!", state="complete", expanded=False)
                    st.success("Pipeline executed successfully. Dashboard and Insights are updated.")
                    time.sleep(2)
                    st.rerun()
                else:
                    status.update(label="❌ Pipeline Failed", state="error", expanded=True)
                    st.error("There was an error in the pipeline. Check the logs above.")

    st.markdown("---")
    st.markdown("### Recent Runs")
    try:
        conn = get_db_conn()
        df_runs = pd.read_sql_query("SELECT start_time, end_time, duration_seconds as duration_s, new_reviews_count as new_reviews, error_count FROM runs ORDER BY id DESC LIMIT 10", conn)
        conn.close()
        st.dataframe(df_runs, use_container_width=True, hide_index=True)
    except:
        st.info("No run history available.")

# ==========================================
# TAB 3: INSIGHTS REPORT
# ==========================================
with tab3:
    st.header("📄 Insights Report")
    
    os.makedirs('reports', exist_ok=True)
    reports = glob.glob('reports/insight_report_*.md')
    
    if not reports:
        st.info("No insight reports generated yet. Go to the Refresh tab to run the pipeline.")
    else:
        # Sort to get latest
        reports.sort(reverse=True)
        selected_report = st.selectbox("Select Report to View", reports)
        
        colA, colB = st.columns([4, 1])
        with colB:
            if st.button("📥 Export as PDF", use_container_width=True):
                pdf_path = selected_report.replace(".md", ".pdf")
                with st.spinner("Generating PDF..."):
                    success = export_report_to_pdf(selected_report, pdf_path)
                    if success:
                        st.success("PDF ready!")
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button("Download PDF", pdf_file, file_name=os.path.basename(pdf_path), mime="application/pdf")
                    else:
                        st.error("Failed to generate PDF.")
                        
        with open(selected_report, 'r', encoding='utf-8') as f:
            md_content = f.read()
            
        st.markdown(md_content)

# ==========================================
# TAB 4: Q&A
# ==========================================
with tab4:
    st.header("💬 Ask your Data")
    st.markdown("Chat with Gemini 2.5, contextualized entirely on your user reviews.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question like: What do power users hate about Discovery?"):
        if len(prompt.strip()) < 2:
            st.error("Please enter a longer question.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response_stream = stream_answer(prompt)
                response = st.write_stream(response_stream)
            st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================
# TAB 5: UPLOAD SOCIAL DATA
# ==========================================
with tab5:
    st.header("📤 Manual Social Media Upload")
    st.markdown("Since social media platforms block automated scraping, you can manually export data and upload it here.")
    
    st.markdown("### Required CSV Format")
    st.markdown("Your CSV file must contain `platform` and `content`. Optional: `date`, `url`.")
    
    sample_data = {
        "platform": ["twitter", "instagram"],
        "content": ["Spotify discover weekly is amazing!", "Why is the algorithm broken today?"],
        "date": ["2026-06-19", "2026-06-18"],
        "url": ["https://twitter.com/x/1", "https://instagram.com/p/2"]
    }
    st.dataframe(pd.DataFrame(sample_data), hide_index=True)
    
    uploaded_file = st.file_uploader("Upload Social CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df_upload = pd.read_csv(uploaded_file)
            st.success("File parsed successfully!")
            st.dataframe(df_upload.head())
            
            if st.button("Process & Insert to Database", use_container_width=True):
                conn = get_db_conn()
                cursor = conn.cursor()
                now = datetime.datetime.now().isoformat()
                inserted = 0
                for _, row in df_upload.iterrows():
                    source = str(row.get('platform', 'social')).lower()
                    text = row.get('content', '')
                    date_val = str(row.get('date', now))
                    url = str(row.get('url', ''))
                    
                    if not pd.isna(text) and str(text).strip():
                        # Generate hash so we avoid duplicates
                        from agents._common import generate_hash
                        item_hash = generate_hash(source, date_val, str(text))
                        try:
                            cursor.execute('''
                                INSERT INTO reviews (source, date, text, url, scraped_at, hash)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (source, date_val, str(text), url, now, item_hash))
                            inserted += 1
                        except sqlite3.IntegrityError:
                            pass # duplicate
                conn.commit()
                conn.close()
                st.success(f"Inserted {inserted} new reviews! Go to the 'Refresh Data' tab and run the master pipeline to tag them.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")

