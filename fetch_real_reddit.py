import sqlite3
import requests
import datetime
import xml.etree.ElementTree as ET
from agents._common import generate_hash

def run():
    print("Fetching real Reddit data via RSS...")
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    
    subreddits = ['spotify', 'truespotify']
    total_new = 0
    now = datetime.datetime.now().isoformat()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for sub in subreddits:
        url = f'https://www.reddit.com/r/{sub}/new.rss'
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                root = ET.fromstring(r.content)
                # Atom namespace
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                
                for entry in root.findall('atom:entry', ns):
                    title = entry.find('atom:title', ns).text or ''
                    content_el = entry.find('atom:content', ns)
                    content = content_el.text if content_el is not None else ''
                    
                    # basic html strip
                    content = content.replace('<p>', '').replace('</p>', '\n').replace('<span>', '').replace('</span>', '')
                    
                    link_el = entry.find('atom:link', ns)
                    url_link = link_el.attrib['href'] if link_el is not None else ''
                    
                    date_str = entry.find('atom:updated', ns).text
                    
                    full_text = f"{title}\n{content}".strip()
                    
                    if not full_text: continue
                    
                    item_hash = generate_hash('reddit', date_str, full_text)
                    
                    theme = 'other'
                    
                    lower_text = full_text.lower()
                    
                    if 'ad ' in lower_text or 'ads ' in lower_text: theme = 'ads'
                    elif 'price' in lower_text or 'pay' in lower_text or 'premium' in lower_text: theme = 'pricing'
                    elif 'shuffle' in lower_text or 'playlist' in lower_text: theme = 'playlist_issues'
                    elif 'sound' in lower_text or 'audio' in lower_text: theme = 'audio_quality'
                    elif 'recommend' in lower_text or 'algorithm' in lower_text: theme = 'recommendation_quality'
                    elif 'crash' in lower_text or 'bug' in lower_text or 'login' in lower_text: theme = 'onboarding_issues'
                    
                    summary = f"Reddit user discussed: {title[:50]}..."
                    
                    try:
                        cursor.execute('''
                            INSERT INTO reviews (source, country, date, rating, text, url, scraped_at, hash, 
                                theme, pain_severity, behavior_intent, summary, tagged_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            'reddit', None, date_str, 0, full_text, url_link, now, item_hash,
                            theme, 3, 'Unknown', summary, now
                        ))
                        total_new += 1
                    except sqlite3.IntegrityError:
                        pass
        except Exception as e:
            print(f"Failed for r/{sub}: {e}")
            
    conn.commit()
    conn.close()
    print(f"Successfully fetched and tagged {total_new} REAL Reddit posts.")

if __name__ == '__main__':
    run()
