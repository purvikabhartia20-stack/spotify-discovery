import sqlite3
import os

db_path = 'data/reviews.db'

# Ensure directory exists
os.makedirs('data', exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create reviews table
cursor.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    country TEXT,
    date TEXT,
    rating INTEGER,
    text TEXT,
    url TEXT,
    scraped_at TEXT,
    theme TEXT,
    pain_severity INTEGER,
    behavior_intent TEXT,
    summary TEXT,
    tagged_at TEXT,
    hash TEXT UNIQUE
)
''')

# Create runs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT,
    end_time TEXT,
    duration_seconds INTEGER,
    new_reviews_count INTEGER,
    tagged_count INTEGER,
    error_count INTEGER
)
''')

# Create sources table
cursor.execute('''
CREATE TABLE IF NOT EXISTS sources (
    source TEXT PRIMARY KEY,
    last_scraped_at TEXT
)
''')

conn.commit()
conn.close()

print("Database initialized successfully at data/reviews.db")
