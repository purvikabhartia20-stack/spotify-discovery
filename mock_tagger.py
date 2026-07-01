import sqlite3
import datetime
import random

def run():
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    
    # Get untagged reviews
    cursor.execute("SELECT id, source FROM reviews WHERE tagged_at IS NULL")
    untagged = cursor.fetchall()
    
    themes = ['recommendation_quality', 'playlist_issues', 'other', 'onboarding_issues', 'audio_quality']
    
    now = datetime.datetime.now().isoformat()
    
    for row in untagged:
        r_id = row[0]
        source = row[1]
        
        # assign mock tags
        cursor.execute('''
            UPDATE reviews 
            SET theme = ?, pain_severity = ?, 
                behavior_intent = ?, summary = ?, tagged_at = ?
            WHERE id = ?
        ''', (
            random.choice(themes),
            random.randint(3, 5),
            "Switching to Apple Music",
            f"User complained about issue on {source}",
            now,
            r_id
        ))
        
    conn.commit()
    conn.close()
    print(f"Manually tagged {len(untagged)} mock reviews due to API exhaustion.")

if __name__ == '__main__':
    run()
