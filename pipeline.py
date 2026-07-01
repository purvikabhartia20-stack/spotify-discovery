import sys
import os
import time
import datetime
import subprocess
import yaml
import sqlite3
import glob
import atexit

def print_banner():
    print("=" * 60)
    print(f"Spotify Discovery Engine Pipeline")
    print(f"Started at: {datetime.datetime.now().isoformat()}")
    print("=" * 60)

def load_config():
    if not os.path.exists('config.yaml'):
        print("Error: config.yaml not found.")
        sys.exit(1)
        
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        
    api_key = config.get('gemini', {}).get('api_key')
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY':
        print("Error: Gemini API key missing in config.yaml. Get one at aistudio.google.com")
        sys.exit(1)

def log_run(start_time, end_time, duration, new_reviews, tagged_count, error_count):
    os.makedirs('data', exist_ok=True)
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO runs (start_time, end_time, duration_seconds, new_reviews_count, tagged_count, error_count)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (start_time, end_time, duration, new_reviews, tagged_count, error_count))
    conn.commit()
    conn.close()

def run_script(script_path, step_num, step_name):
    print(f"\n[Step {step_num}] {step_name}...")
    try:
        # Run subprocess and stream output
        result = subprocess.run([sys.executable, script_path], check=False, capture_output=True, text=True, env={**os.environ, "PYTHONUTF8": "1"})
        
        if result.returncode != 0:
            print(f"  -> {step_name} completed with errors (Exit Code {result.returncode})")
            print(f"  -> Error Output: {result.stderr.strip()}")
            return False
            
        print(f"  -> {step_name} completed successfully.")
        return True
    except Exception as e:
        print(f"  -> Failed to run {script_path}: {e}")
        return False

def count_untagged():
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE tagged_at IS NULL")
    c = cursor.fetchone()[0]
    conn.close()
    return c

def count_total():
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews")
    c = cursor.fetchone()[0]
    conn.close()
    return c

def main():
    if os.path.exists('pipeline.lock'):
        print("Error: Pipeline is already running (pipeline.lock exists). Aborting.")
        sys.exit(1)
        
    with open('pipeline.lock', 'w') as f:
        f.write(str(os.getpid()))
        
    def cleanup_lock():
        if os.path.exists('pipeline.lock'):
            os.remove('pipeline.lock')
            
    atexit.register(cleanup_lock)

    print_banner()
    load_config()
    
    start_time = datetime.datetime.now()
    start_total_reviews = count_total()
    error_count = 0
    
    # 1-4. Scrapers
    scrapers = [
        ('agents/scrape_playstore.py', 'Scraping Play Store'),
        ('fetch_real_apple.py', 'Scraping Apple (iTunes RSS)'),
        ('agents/scrape_reddit.py', 'Scraping Reddit'),
        ('agents/scrape_youtube.py', 'Scraping YouTube')
    ]
    
    for i, (script, name) in enumerate(scrapers):
        success = run_script(script, i+1, name)
        if not success:
            error_count += 1
            

    
    end_total_reviews = count_total()
    new_reviews_found = end_total_reviews - start_total_reviews
    
    untagged_count = count_untagged()
    
    if untagged_count > 0:
        print(f"\nFound {untagged_count} untagged reviews. Running Tagger...")
        success = run_script('agents/tag_reviews.py', '7', 'Tagging Reviews')
        if not success:
            error_count += 1
    else:
        print("\n[Step 7] Tagging Reviews... skipped (no new reviews)")
        
    # 8. Synthesize
    success = run_script('agents/synthesize.py', '8', 'Synthesizing Report')
    if not success:
        error_count += 1
        
    end_time = datetime.datetime.now()
    duration = int((end_time - start_time).total_seconds())
    
    log_run(start_time.isoformat(), end_time.isoformat(), duration, new_reviews_found, untagged_count, error_count)
    
    print("\n" + "=" * 60)
    print(f"[SUCCESS] Refresh complete.")
    print(f"  -> {new_reviews_found} new reviews added.")
    print(f"  -> {untagged_count} reviews tagged.")
    print(f"  -> Reports saved to reports/ folder.")
    if error_count > 0:
        print(f"  -> Note: {error_count} steps encountered errors (check output).")
    print("=" * 60)

if __name__ == '__main__':
    main()
