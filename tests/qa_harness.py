import os
import sys
import time
import subprocess
import sqlite3
import pandas as pd
import datetime

# Add parent directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.qa import stream_answer

def run_test(name, func):
    print(f"\n{'='*60}")
    print(f"RUNNING TEST: {name}")
    print(f"{'='*60}")
    try:
        func()
        print(f"\n[PASS] {name}")
    except Exception as e:
        print(f"\n[FAIL] {name}")
        print(f"Error: {e}")

def test_1_fresh_setup():
    db_path = 'data/reviews.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Deleted existing database.")
        
    subprocess.run([sys.executable, "init_db.py"], check=True)
    
    # We can't fully simulate the Streamlit UI, but we can verify the DB is gone
    if not os.path.exists(db_path):
        raise Exception("Failed to re-initialize database.")
    print("Database deleted. Dashboard will show empty state.")

def test_2_first_refresh():
    start_time = time.time()
    result = subprocess.run([sys.executable, "pipeline.py"], capture_output=True, text=True, env={**os.environ, "PYTHONUTF8": "1"})
    duration = time.time() - start_time
    print(f"Pipeline output tail:\n{result.stdout[-500:]}")
    
    if result.returncode != 0:
        raise Exception(f"Pipeline failed with exit code {result.returncode}")
        
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews")
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Added {count} reviews in {duration:.1f} seconds.")
    if count < 100:
        raise Exception("Not enough reviews added.")

def test_3_incremental_refresh():
    start_time = time.time()
    result = subprocess.run([sys.executable, "pipeline.py"], capture_output=True, text=True, env={**os.environ, "PYTHONUTF8": "1"})
    duration = time.time() - start_time
    print(f"Pipeline output tail:\n{result.stdout[-500:]}")
    
    if result.returncode != 0:
        raise Exception(f"Pipeline failed with exit code {result.returncode}")
        
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews")
    count = cursor.fetchone()[0]
    conn.close()
    
    print(f"Total reviews: {count}. Completed in {duration:.1f} seconds.")
    if duration > 180: # 3 minutes
        raise Exception(f"Incremental refresh took too long: {duration} seconds")

def test_4_social_upload():
    csv_path = 'data/social_uploads/test_social.csv'
    if not os.path.exists(csv_path):
        raise Exception(f"Test CSV not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    now = datetime.datetime.now().isoformat()
    inserted = 0
    for _, row in df.iterrows():
        source = str(row.get('source', 'social')).lower()
        text = row.get('text', '')
        date_val = str(row.get('date', now))
        url = str(row.get('link', ''))
        
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
    
    print(f"Inserted {inserted} social reviews.")
    if inserted == 0:
        raise Exception("Failed to insert any social reviews.")

def test_6_qa():
    questions = [
        "What do casual listeners say about Discover Weekly?",
        "Why do power users complain about recommendations?",
        "What features do users wish existed?",
        "Is mood-based discovery working for users?",
        "What's the most common reason users keep listening to the same songs?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        stream = stream_answer(q)
        ans = ""
        for chunk in stream:
            ans += chunk
        print(f"A: {ans}")
        if len(ans) < 50:
            raise Exception(f"Answer seems too short or failed: {ans}")

if __name__ == "__main__":
    # run_test("Test 1: Fresh setup", test_1_fresh_setup)
    # run_test("Test 2: First-ever refresh", test_2_first_refresh)
    run_test("Test 3: Incremental refresh", test_3_incremental_refresh)
    run_test("Test 4: Social upload", test_4_social_upload)
    run_test("Test 6: Q&A", test_6_qa)
    
    print("\nDONE!")
