import sys
import os
import logging
import time

# Add the parent directory to sys.path so we can import _common
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import save_reviews, is_within_90_days, logging

from app_store_scraper import AppStore

def run():
    print("Starting App Store Scraper...")
    logging.info("Starting App Store Scraper")
    app_name = 'spotify-music-and-podcasts'
    app_id = 324684580
    countries = ['us', 'gb', 'in', 'de']
    
    # Volume Limit for App Store: 300 reviews total
    MAX_REVIEWS_PER_COUNTRY = 150
    TOTAL_LIMIT = 300
    
    all_valid_reviews = []
    
    for country in countries:
        if len(all_valid_reviews) >= TOTAL_LIMIT:
            break
            
        print(f"Fetching App Store reviews for {country.upper()}...")
        try:
            scraper = AppStore(country=country, app_name=app_name, app_id=app_id)
            # AppStore scraper fetches all if count not provided. It handles pagination.
            # We use how_many to limit initial pull.
            scraper.review(how_many=MAX_REVIEWS_PER_COUNTRY)
            
            valid_for_country = 0
            for r in scraper.reviews:
                if len(all_valid_reviews) >= TOTAL_LIMIT:
                    break
                    
                date_val = r.get('date')
                if not is_within_90_days(date_val):
                    continue
                    
                # Clean text
                text = r.get('review', '')
                if text and len(text) > 4000:
                    text = text[:4000]
                    
                review_obj = {
                    'source': 'appstore',
                    'country': country.upper(),
                    'date': date_val.isoformat() if date_val else None,
                    'rating': r.get('rating'),
                    'text': text,
                    'url': None
                }
                all_valid_reviews.append(review_obj)
                valid_for_country += 1
                
            print(f"  -> Found {valid_for_country} recent reviews.")
            
            # Apple rate limit avoidance
            time.sleep(2)
        except Exception as e:
            print(f"  -> Error fetching for {country}: {e}")
            logging.error(f"AppStore scraper error for {country}: {e}")
            time.sleep(5) # backoff on error
            
    print(f"Total valid recent App Store reviews collected: {len(all_valid_reviews)}")
    
    # Save to DB
    new_count = save_reviews(all_valid_reviews)
    print(f"App Store Scraper finished. {new_count} new reviews saved to database.\n")
    logging.info(f"App Store Scraper finished. {new_count} new saved.")

if __name__ == '__main__':
    run()
