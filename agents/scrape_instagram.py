import sys
import os
import logging
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import save_reviews, is_within_90_days, logging

import instaloader

def run():
    print("Starting Instagram Scraper...")
    logging.info("Starting Instagram Scraper")
    
    hashtags = ["spotify", "spotifywrapped", "spotifyplaylist"]
    
    TOTAL_LIMIT = 50
    all_valid_posts = []
    
    try:
        L = instaloader.Instaloader(quiet=True)
        
        for tag in hashtags:
            if len(all_valid_posts) >= TOTAL_LIMIT:
                break
                
            print(f"Searching Instagram for #{tag}...")
            try:
                # Fetch recent posts for hashtag
                posts = instaloader.Hashtag.from_name(L.context, tag).get_posts()
                
                count = 0
                for post in posts:
                    if len(all_valid_posts) >= TOTAL_LIMIT:
                        break
                    
                    # We only look at a max of 20 posts per hashtag to not get banned
                    if count >= 20:
                        break
                    count += 1
                        
                    dt = post.date
                    if dt and not is_within_90_days(dt):
                        continue
                        
                    text = post.caption if post.caption else ''
                    
                    if not text:
                        continue
                        
                    if len(text) > 4000:
                        text = text[:4000]
                        
                    shortcode = post.shortcode
                    url = f"https://www.instagram.com/p/{shortcode}/" if shortcode else None
                    
                    review_obj = {
                        'source': 'instagram',
                        'country': None,
                        'date': dt.isoformat() if dt else datetime.datetime.now().isoformat(),
                        'rating': None,
                        'text': text,
                        'url': url
                    }
                    all_valid_posts.append(review_obj)
                    
                    time.sleep(1) # Polite delay
                
                time.sleep(2)
                
            except Exception as e:
                print(f"  -> Error fetching Instagram #{tag}: {e}")
                logging.error(f"Instagram scraper error for #{tag}: {e}")
                
    except Exception as e:
        print(f"Failed to initialize Instaloader: {e}")
        logging.error(f"Instagram scraper init error: {e}")
        
    print(f"Total valid recent Instagram posts collected: {len(all_valid_posts)}")
    
    new_count = save_reviews(all_valid_posts)
    print(f"Instagram Scraper finished. {new_count} new posts saved to database.\n")
    logging.info(f"Instagram Scraper finished. {new_count} new saved.")

if __name__ == '__main__':
    run()
