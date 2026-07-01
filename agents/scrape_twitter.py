import sys
import os
import logging
import time
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import save_reviews, is_within_90_days, logging

from ntscraper import Nitter

def run():
    print("Starting Twitter Scraper...")
    logging.info("Starting Twitter Scraper")
    
    terms = ["spotify discovery", "spotify discover weekly", "spotify algorithm bad"]
    
    TOTAL_LIMIT = 50
    all_valid_tweets = []
    
    try:
        scraper = Nitter()
        
        for term in terms:
            if len(all_valid_tweets) >= TOTAL_LIMIT:
                break
                
            print(f"Searching Twitter for: '{term}'...")
            try:
                # Get tweets
                results = scraper.get_tweets(term, mode='term', number=20)
                tweets = results.get('tweets', [])
                
                for t in tweets:
                    if len(all_valid_tweets) >= TOTAL_LIMIT:
                        break
                        
                    date_str = t.get('date') # Format: "Dec 30, 2023 · 8:12 PM UTC"
                    dt = None
                    if date_str:
                        # Nitter date format parsing can be tricky, we'll try a rough parse
                        try:
                            # Try to extract just the date part "Dec 30, 2023"
                            clean_date = date_str.split('·')[0].strip()
                            dt = datetime.datetime.strptime(clean_date, "%b %d, %Y")
                        except Exception:
                            # fallback to now if we can't parse Nitter's weird string
                            dt = datetime.datetime.now()
                            
                    if dt and not is_within_90_days(dt):
                        continue
                        
                    text = t.get('text', '')
                    if not text:
                        continue
                        
                    if len(text) > 4000:
                        text = text[:4000]
                        
                    url = t.get('link')
                    
                    review_obj = {
                        'source': 'twitter',
                        'country': None,
                        'date': dt.isoformat() if dt else datetime.datetime.now().isoformat(),
                        'rating': None,
                        'text': text,
                        'url': url
                    }
                    all_valid_tweets.append(review_obj)
                    
                time.sleep(2) # Polite delay
                
            except Exception as e:
                print(f"  -> Error fetching tweets for '{term}': {e}")
                logging.error(f"Twitter scraper error for term '{term}': {e}")
                
    except Exception as e:
        print(f"Failed to initialize Nitter: {e}")
        logging.error(f"Twitter scraper init error: {e}")
        
    print(f"Total valid recent Tweets collected: {len(all_valid_tweets)}")
    
    new_count = save_reviews(all_valid_tweets)
    print(f"Twitter Scraper finished. {new_count} new tweets saved to database.\n")
    logging.info(f"Twitter Scraper finished. {new_count} new saved.")

if __name__ == '__main__':
    run()
