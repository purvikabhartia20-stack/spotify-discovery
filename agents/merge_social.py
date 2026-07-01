import sys
import os
import csv
import shutil
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import save_reviews, logging

def merge_csv(filepath):
    print(f"Processing social CSV: {filepath}")
    
    required_cols = {'source', 'date', 'text', 'link'}
    
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                print(f"Error: CSV {filepath} is empty or malformed.")
                return 0
                
            header = set(reader.fieldnames)
            missing = required_cols - header
            if missing:
                print(f"Error: CSV {filepath} missing required columns: {missing}")
                print(f"Expected: {required_cols}")
                print(f"Found: {header}")
                return 0
                
            social_reviews = []
            for row in reader:
                text = row.get('text', '').strip()
                if not text:
                    continue
                    
                review_obj = {
                    'source': f"social_{row.get('source', 'unknown').strip().lower()}",
                    'country': None,
                    'date': row.get('date'),
                    'rating': None,
                    'text': text,
                    'url': row.get('link')
                }
                social_reviews.append(review_obj)
                
            if not social_reviews:
                print("No valid rows found in CSV.")
                return 0
                
            new_count = save_reviews(social_reviews)
            print(f"Added {new_count} new social posts to the corpus from {os.path.basename(filepath)}")
            
        # Move to processed (OUTSIDE the with block to avoid Windows file locks)
        processed_dir = os.path.join(os.path.dirname(filepath), 'processed')
        os.makedirs(processed_dir, exist_ok=True)
        shutil.move(filepath, os.path.join(processed_dir, os.path.basename(filepath)))
        
        return new_count
            
    except Exception as e:
        print(f"Failed to process CSV {filepath}: {e}")
        logging.error(f"Failed to process CSV {filepath}: {e}")
        return 0

if __name__ == '__main__':
    if len(sys.argv) > 1:
        merge_csv(sys.argv[1])
    else:
        print("Usage: python merge_social.py <path_to_csv>")
