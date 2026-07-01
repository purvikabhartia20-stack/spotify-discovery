import sys
import os
import json
import time
import datetime
import logging
import sqlite3
import yaml
import re
import google.generativeai as genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import get_db_connection

def load_config():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def clean_json_response(text):
    """Strip markdown code fences and get raw json."""
    text = text.strip()
    # Remove markdown formatting if present
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
        
    if text.endswith("```"):
        text = text[:-3]
        
    return text.strip()

def tag_batch(model, batch, prompt_template):
    # Prepare reviews JSON
    reviews_data = []
    for r in batch:
        # Token Saving: Truncate text
        text = r['text']
        max_len = 800 if r['source'] == 'youtube' else 150
        if text and len(text) > max_len:
            text = text[:max_len] + "..."
            
        reviews_data.append({
            "review_id": r['id'],
            "text": text
        })
        
    reviews_json_str = json.dumps(reviews_data, indent=2)
    prompt = prompt_template.replace('{reviews_json}', reviews_json_str)
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Gemini API call failed: {error_msg}")
        if "429" in error_msg or "ResourceExhausted" in error_msg or "Quota" in error_msg:
            return "QUOTA_EXCEEDED"
        return None

def run():
    print("Starting Tagger...")
    config = load_config()
    api_key = config.get('gemini', {}).get('api_key')
    
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY':
        print("Gemini API key missing in config.yaml.")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Load prompt
    prompt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prompts', 'tag_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()
        
    os.makedirs('data/failed_batches', exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reviews WHERE tagged_at IS NULL")
    untagged = cursor.fetchall()
    
    if not untagged:
        print("Zero reviews to tag.")
        return
        
    print(f"Found {len(untagged)} untagged reviews. Starting batching...")
    
    batch_size = 20
    total_tagged = 0
    total_failed = 0
    
    for i in range(0, len(untagged), batch_size):
        batch = untagged[i:i+batch_size]
        print(f"Tagging {i + len(batch)}/{len(untagged)}...")
        
        # Retry loop
        success = False
        for attempt in range(2):
            raw_response = tag_batch(model, batch, prompt_template)
            
            if raw_response == "QUOTA_EXCEEDED":
                print("\n  -> 🚨 Gemini API Daily Quota Exceeded!")
                print(f"  -> Successfully tagged {total_tagged} reviews this run.")
                print(f"  -> {len(untagged) - total_tagged} reviews remain untagged and will be tagged tomorrow.")
                return # Exit the script entirely so the pipeline can continue!
                
            if not raw_response:
                print("  -> API call failed. Sleeping 60s.")
                time.sleep(60)
                continue
                
            clean_str = clean_json_response(raw_response)
            
            try:
                tagged_data = json.loads(clean_str)
                # Ensure it's a list
                if not isinstance(tagged_data, list):
                    raise ValueError("Response is not a JSON array")
                    
                # Update DB
                tagged_at = datetime.datetime.now().isoformat()
                for item in tagged_data:
                    rid = item.get('review_id')
                    cursor.execute('''
                        UPDATE reviews 
                        SET theme=?, pain_severity=?, behavior_intent=?, summary=?, tagged_at=?
                        WHERE id=?
                    ''', (
                        item.get('theme'),
                        item.get('pain_severity'),
                        item.get('behavior_intent'),
                        item.get('summary'),
                        tagged_at,
                        rid
                    ))
                conn.commit()
                success = True
                total_tagged += len(batch)
                break # break retry loop
                
            except json.JSONDecodeError:
                print(f"  -> JSON parse failed on attempt {attempt+1}")
                # Log failed batch output on last attempt
                if attempt == 1:
                    failed_log_path = f"data/failed_batches/batch_{i}_{int(time.time())}.txt"
                    with open(failed_log_path, 'w', encoding='utf-8') as f:
                        f.write(raw_response)
                    total_failed += len(batch)
            except Exception as e:
                print(f"  -> Unexpected error: {e}")
                
        # API rate limits politeness
        time.sleep(5)
        
    print("\n--- Tagging Complete ---")
    print(f"Total Tagged: {total_tagged}")
    print(f"Total Failed: {total_failed}")

if __name__ == '__main__':
    run()
