import sys
import os
import logging
import time
import requests
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import save_reviews, is_within_90_days, logging

def run():
    print("Starting Reddit Scraper...")
    logging.info("Starting Reddit Scraper")
    
    subreddits = ['spotify', 'Music', 'truespotify', 'SpotifyThrowbacks', 'LetsTalkMusic']
    search_terms = ["discover weekly", "release radar", "recommendations", "algorithm", "for you", "daily mix", "music discovery"]
    
    TOTAL_LIMIT = 100
    all_valid_posts = []
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for sub in subreddits:
        if len(all_valid_posts) >= TOTAL_LIMIT:
            break
            
        print(f"Searching r/{sub}...")
        for term in search_terms:
            if len(all_valid_posts) >= TOTAL_LIMIT:
                break
                
            try:
                # Use reddit RSS endpoint
                url = f"https://www.reddit.com/r/{sub}/search.rss?q={term}&restrict_sr=1&sort=new&limit=25"
                resp = requests.get(url, headers=headers, timeout=10)
                
                if resp.status_code == 429:
                    print("  -> Rate limited! Sleeping for 10 seconds.")
                    time.sleep(10)
                    continue
                elif resp.status_code != 200:
                    print(f"  -> Failed with status {resp.status_code}")
                    continue
                    
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(resp.content)
                except Exception as parse_err:
                    print(f"  -> XML Parse Error: {parse_err}")
                    continue
                
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                children = root.findall('atom:entry', ns)
                
                valid_count = 0
                for entry in children:
                    if len(all_valid_posts) >= TOTAL_LIMIT:
                        break
                        
                    title = entry.find('atom:title', ns).text or ''
                    content_el = entry.find('atom:content', ns)
                    body = content_el.text if content_el is not None else ''
                    
                    # basic html strip
                    body = body.replace('<p>', '').replace('</p>', '\n').replace('<span>', '').replace('</span>', '')
                    
                    date_str = entry.find('atom:updated', ns).text
                    if not date_str:
                        continue
                        
                    # parse date string like 2026-06-21T18:00:00+00:00
                    try:
                        dt = datetime.datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    except:
                        dt = datetime.datetime.now()
                        
                    if not is_within_90_days(dt):
                        continue
                        
                    combined_text = f"{title}\n{body}".strip()
                    
                    if len(combined_text) > 4000:
                        combined_text = combined_text[:4000]
                        
                    if not combined_text:
                        continue
                        
                    link_el = entry.find('atom:link', ns)
                    full_url = link_el.attrib['href'] if link_el is not None else None
                    
                    review_obj = {
                        'source': 'reddit',
                        'country': None,
                        'date': dt.isoformat(),
                        'rating': 0, # RSS doesn't give score easily
                        'text': combined_text,
                        'url': full_url
                    }
                    all_valid_posts.append(review_obj)
                    valid_count += 1
                
                # Polite delay
                time.sleep(2)
                
            except Exception as e:
                print(f"  -> Error fetching r/{sub} for term '{term}': {e}")
                logging.error(f"Reddit scraper error r/{sub} term '{term}': {e}")
                time.sleep(5)
                
    print(f"Total valid recent Reddit posts collected: {len(all_valid_posts)}")
    
    new_count = save_reviews(all_valid_posts)
    print(f"Reddit Scraper finished. {new_count} new posts saved to database.\n")
    logging.info(f"Reddit Scraper finished. {new_count} new saved.")

if __name__ == '__main__':
    run()
