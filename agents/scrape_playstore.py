import sys
import os
import logging

# Add the parent directory to sys.path so we can import _common
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import save_reviews, is_within_90_days, logging

from google_play_scraper import Sort, reviews

def run():
    print("Starting Play Store Scraper...")
    logging.info("Starting Play Store Scraper")
    app_id = 'com.spotify.music'
    countries = ['us', 'gb', 'in', 'de']
    
    # Volume Limit for Play Store: 500 reviews
    # We will fetch up to 200 per country to find 500 total valid 90-day reviews, but stop as soon as we hit 500 total new ones.
    MAX_REVIEWS_PER_COUNTRY = 200
    TOTAL_LIMIT = 500
    
    all_valid_reviews = []
    
    for country in countries:
        if len(all_valid_reviews) >= TOTAL_LIMIT:
            break
            
        print(f"Fetching Play Store reviews for {country.upper()}...")
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en', # fetch english reviews mostly
                country=country,
                sort=Sort.NEWEST,
                count=MAX_REVIEWS_PER_COUNTRY
            )
            
            valid_for_country = 0
            for r in result:
                if len(all_valid_reviews) >= TOTAL_LIMIT:
                    break
                    
                date_val = r.get('at')
                if not is_within_90_days(date_val):
                    continue
                    
                # Clean text: truncate super long reviews
                text = r.get('content', '')
                if text and len(text) > 4000:
                    text = text[:4000]
                    
                review_obj = {
                    'source': 'playstore',
                    'country': country.upper(),
                    'date': date_val.isoformat() if date_val else None,
                    'rating': r.get('score'),
                    'text': text,
                    'url': None # Google play scraper doesn't give direct review URLs easily
                }
                all_valid_reviews.append(review_obj)
                valid_for_country += 1
                
            print(f"  -> Found {valid_for_country} recent reviews.")
        except Exception as e:
            print(f"  -> Error fetching for {country}: {e}")
            logging.error(f"PlayStore scraper error for {country}: {e}")
            
    print(f"Total valid recent Play Store reviews collected: {len(all_valid_reviews)}")
    
    # Save to DB
    new_count = save_reviews(all_valid_reviews)
    print(f"Play Store Scraper finished. {new_count} new reviews saved to database.\n")
    logging.info(f"Play Store Scraper finished. {new_count} new saved.")

if __name__ == '__main__':
    run()
