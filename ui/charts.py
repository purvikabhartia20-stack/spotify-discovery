import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

def get_db_conn():
    return sqlite3.connect('data/reviews.db')

def plot_theme_breakdown():
    conn = get_db_conn()
    df = pd.read_sql_query("SELECT theme, COUNT(*) as count FROM reviews WHERE tagged_at IS NOT NULL AND theme != 'other' GROUP BY theme ORDER BY count DESC", conn)
    conn.close()
    
    if df.empty:
        return None
        
    # Clean up theme names for display
    df['theme'] = df['theme'].str.replace('_', ' ').str.title()
    
    fig = px.bar(
        df, 
        x='count', 
        y='theme', 
        orientation='h',
        title="Top Pain Points (by Volume)",
        color_discrete_sequence=['#1DB954']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        yaxis={'categoryorder':'total ascending'}
    )
    return fig


def get_recent_high_severity():
    conn = get_db_conn()
    df = pd.read_sql_query("""
        SELECT date, source, theme, pain_severity as severity, text 
        FROM reviews 
        WHERE tagged_at IS NOT NULL AND pain_severity >= 3
        ORDER BY date DESC LIMIT 5
    """, conn)
    conn.close()
    return df

def plot_review_volume_over_time():
    conn = get_db_conn()
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m-%d', date) as day, COUNT(*) as count 
        FROM reviews 
        WHERE date IS NOT NULL
        GROUP BY day
        ORDER BY day
    """, conn)
    conn.close()
    
    if df.empty:
        return None
        
    fig = px.bar(
        df, 
        x='day', 
        y='count', 
        title="Review Volume Over Time",
        color_discrete_sequence=['#1DB954']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        xaxis_title="Date",
        yaxis_title="Volume",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def plot_severity_by_theme():
    conn = get_db_conn()
    df = pd.read_sql_query("""
        SELECT theme, AVG(pain_severity) as avg_severity 
        FROM reviews 
        WHERE tagged_at IS NOT NULL AND theme != 'other'
        GROUP BY theme
        ORDER BY avg_severity DESC
    """, conn)
    conn.close()
    
    if df.empty:
        return None
        
    df['theme'] = df['theme'].str.replace('_', ' ').str.title()
    
    fig = px.bar(
        df, 
        x='theme', 
        y='avg_severity', 
        title="Average Severity by Theme",
        color_discrete_sequence=['#e91429']
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        xaxis_title="Theme",
        yaxis_title="Average Severity",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def plot_reviews_by_source():
    conn = get_db_conn()
    df = pd.read_sql_query("""
        SELECT source, COUNT(*) as count 
        FROM reviews 
        GROUP BY source
        ORDER BY count DESC
    """, conn)
    conn.close()
    
    if df.empty:
        return None
        
    df['source'] = df['source'].str.title()
    
    fig = px.pie(
        df, 
        values='count', 
        names='source', 
        hole=0.6,
        title="Reviews by Platform",
        color_discrete_sequence=px.colors.sequential.Greens_r
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#ffffff',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def get_platform_country_distribution():
    conn = get_db_conn()
    df = pd.read_sql_query("""
        SELECT source as Platform, IFNULL(country, 'Global/Unknown') as Country, COUNT(*) as Reviews
        FROM reviews 
        GROUP BY source, country
        ORDER BY Reviews DESC
    """, conn)
    conn.close()
    
    # Capitalize platform names
    if not df.empty:
        df['Platform'] = df['Platform'].str.title()
        
    return df
