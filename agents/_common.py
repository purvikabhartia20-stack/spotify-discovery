import sqlite3
import hashlib
import os
import datetime
import logging

DB_PATH = 'data/reviews.db'
LOG_PATH = 'data/runs.log'

# Configure basic logging
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_db_connection():
    # SQLite can handle concurrent reads but writes must be careful. We'll use timeout
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn

def generate_hash(source, date, text):
    """Generate a unique hash for deduplication based on source, date, and text."""
    # Handle None values gracefully
    safe_date = str(date) if date else ""
    safe_text = str(text) if text else ""
    raw = f"{source}-{safe_date}-{safe_text}".encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def is_within_90_days(date_val):
    """Check if a date is within the last 90 days. date_val can be datetime or string."""
    if not date_val:
        return False
    
    if isinstance(date_val, str):
        # Try parsing common formats
        try:
            # Assumes YYYY-MM-DD or similar standard format
            dt = datetime.datetime.fromisoformat(date_val.replace('Z', '+00:00'))
        except ValueError:
            # Fallback for simple date parsing if isoformat fails
            # We'll assume it's recent if we can't parse it for now, or just reject it.
            # Rejecting is safer to prevent old junk.
            return False
    elif isinstance(date_val, datetime.datetime):
        dt = date_val
    elif isinstance(date_val, datetime.date):
        dt = datetime.datetime.combine(date_val, datetime.time.min)
    else:
        return False

    # Ensure dt is timezone-naive for comparison if now is naive
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)

    now = datetime.datetime.now()
    delta = now - dt
    return delta.days <= 90

def save_reviews(reviews_list):
    """
    Saves a list of reviews to the database, skipping duplicates.
    reviews_list is a list of dicts with keys: source, country, date, rating, text, url
    Returns the number of new reviews successfully inserted.
    """
    if not reviews_list:
        return 0

    conn = get_db_connection()
    cursor = conn.cursor()
    new_count = 0
    scraped_at = datetime.datetime.now().isoformat()

    for r in reviews_list:
        # Generate hash
        item_hash = generate_hash(r.get('source'), r.get('date'), r.get('text'))
        
        try:
            cursor.execute('''
                INSERT INTO reviews (source, country, date, rating, text, url, scraped_at, hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                r.get('source'),
                r.get('country'),
                r.get('date'),
                r.get('rating'),
                r.get('text'),
                r.get('url'),
                scraped_at,
                item_hash
            ))
            new_count += 1
        except sqlite3.IntegrityError:
            # Hash already exists, duplicate
            pass
        except Exception as e:
            logging.error(f"Error inserting review {item_hash}: {str(e)}")

    # Update sources table
    if reviews_list:
        source_name = reviews_list[0].get('source')
        if source_name:
            cursor.execute('''
                INSERT INTO sources (source, last_scraped_at)
                VALUES (?, ?)
                ON CONFLICT(source) DO UPDATE SET last_scraped_at=excluded.last_scraped_at
            ''', (source_name, scraped_at))

    conn.commit()
    conn.close()
    
    return new_count
