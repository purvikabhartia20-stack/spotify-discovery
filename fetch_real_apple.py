import sqlite3
import requests
import datetime
from agents._common import generate_hash

def run():
    print("Fetching real App Store reviews directly via RSS...")
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    
    countries = ['us', 'gb', 'ca', 'au', 'in']
    app_id = '324684580'
    
    total_new = 0
    now = datetime.datetime.now().isoformat()
    
    for country in countries:
        url = f'https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json'
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                entries = data.get('feed', {}).get('entry', [])
                
                # First entry is sometimes the app info itself, so skip if 'author' is apple
                for entry in entries:
                    if 'author' not in entry: continue
                    
                    text = entry.get('content', {}).get('label', '')
                    title = entry.get('title', {}).get('label', '')
                    rating_str = entry.get('im:rating', {}).get('label', '3')
                    rating = int(rating_str)
                    
                    full_text = f"{title}\n{text}"
                    
                    if not full_text.strip():
                        continue
                        
                    # iTunes RSS doesn't give a perfect date, but we can fake it to today or parse if available
                    # Actually, some feeds have 'updated'
                    date_val = entry.get('updated', {}).get('label', now)
                    
                    item_hash = generate_hash('appstore', date_val, full_text)
                    
                    # Basic keyword tagging since API is exhausted
                    theme = 'other'
                    
                    lower_text = full_text.lower()
                    
                    if 'ad ' in lower_text or 'ads ' in lower_text: theme = 'ads'
                    elif 'price' in lower_text or 'pay' in lower_text or 'premium' in lower_text: theme = 'pricing'
                    elif 'shuffle' in lower_text or 'playlist' in lower_text: theme = 'playlist_issues'
                    elif 'sound' in lower_text or 'audio' in lower_text: theme = 'audio_quality'
                    elif 'recommend' in lower_text or 'algorithm' in lower_text: theme = 'recommendation_quality'
                    elif 'crash' in lower_text or 'bug' in lower_text or 'login' in lower_text: theme = 'onboarding_issues'
                    
                    summary = f"User mentioned: {title}"
                    
                    try:
                        cursor.execute('''
                            INSERT INTO reviews (source, country, date, rating, text, url, scraped_at, hash, 
                                theme, pain_severity, behavior_intent, summary, tagged_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            'appstore', country.upper(), date_val, rating, full_text, None, now, item_hash,
                            theme, 5 if rating==1 else 3, 'Unknown', summary, now
                        ))
                        total_new += 1
                    except sqlite3.IntegrityError:
                        pass
        except Exception as e:
            print(f"Failed for {country}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Successfully fetched and tagged {total_new} REAL App Store reviews.")

if __name__ == '__main__':
    run()
