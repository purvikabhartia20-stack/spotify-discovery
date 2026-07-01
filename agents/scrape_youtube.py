import sys
import os
import time
import datetime
import yaml

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents._common import get_db_connection, generate_hash

from googleapiclient.discovery import build

def run():
    print("Starting Official YouTube Scraper (Comments)...")
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
        
    api_key = config.get('youtube', {}).get('api_key')
    if not api_key:
        print("Error: YouTube API key missing from config.yaml")
        return
        
    youtube = build("youtube", "v3", developerKey=api_key)
    
    queries = [
        "Spotify discover weekly", 
        "Spotify recommendations", 
        "Apple music vs spotify algorithm"
    ]
    
    now = datetime.datetime.now().isoformat()
    total_comments = 0
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    for q in queries:
        try:
            print(f"Searching for '{q}'...")
            search_response = youtube.search().list(
                q=q,
                part="id",
                maxResults=2,
                type="video"
            ).execute()
            
            for search_result in search_response.get("items", []):
                video_id = search_result["id"]["videoId"]
                url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Get comments
                try:
                    comments_response = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        maxResults=20,
                        order="relevance"
                    ).execute()
                    
                    for comment_thread in comments_response.get("items", []):
                        snippet = comment_thread["snippet"]["topLevelComment"]["snippet"]
                        text = snippet["textDisplay"]
                        date_str = snippet["publishedAt"] # e.g. 2026-06-19T10:19:43Z
                        
                        if len(text) < 20 or len(text) > 2000:
                            continue
                            
                        item_hash = generate_hash('youtube', date_str, text)
                        
                        theme = 'other'
                        sentiment = 'neutral'
                        lower_text = text.lower()
                        
                        if 'hate' in lower_text or 'sucks' in lower_text or 'bad' in lower_text or 'issue' in lower_text or 'worse' in lower_text: sentiment = 'negative'
                        elif 'love' in lower_text or 'great' in lower_text or 'good' in lower_text or 'better' in lower_text: sentiment = 'positive'
                        else: sentiment = 'mixed'
                        
                        if 'ad ' in lower_text or 'ads ' in lower_text: theme = 'ads'
                        elif 'price' in lower_text or 'pay' in lower_text or 'premium' in lower_text: theme = 'pricing'
                        elif 'shuffle' in lower_text or 'playlist' in lower_text: theme = 'playlist_issues'
                        elif 'sound' in lower_text or 'audio' in lower_text: theme = 'audio_quality'
                        elif 'recommend' in lower_text or 'algorithm' in lower_text: theme = 'recommendation_quality'
                        elif 'crash' in lower_text or 'bug' in lower_text or 'login' in lower_text: theme = 'onboarding_issues'
                        
                        summary = f"YouTube comment: {text[:50]}..."
                        
                        try:
                            cursor.execute('''
                                INSERT INTO reviews (source, country, date, rating, text, url, scraped_at, hash, 
                                    theme, sentiment, segment, pain_severity, behavior_intent, summary, tagged_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                                'youtube', None, date_str, 0, text, url, now, item_hash,
                                theme, sentiment, 'casual_listener', 3, 'Unknown', summary, now
                            ))
                            total_comments += 1
                        except Exception:
                            pass
                except Exception as e:
                    print(f"  -> Could not fetch comments for video {video_id}: {e}")
        except Exception as e:
            print(f"Failed to search YouTube: {e}")
            
    conn.commit()
    conn.close()
    
    print(f"YouTube Scraper finished. {total_comments} new real comments saved and tagged.")

if __name__ == '__main__':
    run()
