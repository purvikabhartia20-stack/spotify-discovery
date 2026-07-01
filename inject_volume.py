import sqlite3
import datetime
import random

def run():
    print("Injecting high volume of mock data to populate dashboard...")
    
    conn = sqlite3.connect('data/reviews.db')
    cursor = conn.cursor()
    
    now = datetime.datetime.now()
    
    sources = [
        ('appstore', 120),
        ('reddit', 80),
        ('youtube', 40)
    ]
    
    themes = ['pricing', 'ads', 'audio_quality', 'recommendation_quality', 'playlist_issues', 'onboarding_issues', 'search_problems', 'discovery_difficulty']
    
    templates = [
        "The {feature} is completely broken since the last update. I can't even {action}.",
        "Why did they change {feature}? It used to be so good.",
        "Honestly, {feature} is the only reason I still pay for this app.",
        "I've been trying to {action} for 3 days and it just crashes.",
        "Recommendations are okay, but {feature} needs a lot of work.",
        "I love the new {feature}, makes it much easier to {action}!",
        "Can we please get a fix for {feature}?",
        "Anyone else having issues with {feature} today?",
        "Switched from Apple Music and the {feature} here is way better.",
        "The price increase is insane considering {feature} still barely works."
    ]
    
    features = ['Discover Weekly', 'Release Radar', 'Smart Shuffle', 'Lyrics', 'Podcasts section', 'Offline downloads', 'CarPlay integration', 'Desktop app', 'Audio normalization']
    actions = ['find new music', 'play my saved playlists', 'share songs', 'view lyrics', 'download for my flight', 'cast to my TV', 'organize my folders']
    
    total_injected = 0
    
    for source, count in sources:
        for _ in range(count):
            date_val = now - datetime.timedelta(days=random.randint(0, 89), hours=random.randint(0, 23))
            
            theme = random.choice(themes)
                
            template = random.choice(templates)
            text = template.format(feature=random.choice(features), action=random.choice(actions))
            
            # Insert directly as tagged
            cursor.execute('''
                INSERT INTO reviews (
                    source, country, date, rating, text, url, 
                    theme, pain_severity, behavior_intent, summary, tagged_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                source,
                'US' if source == 'appstore' else None,
                date_val.isoformat(),
                random.randint(1, 5) if source == 'appstore' else None,
                text,
                f"https://example.com/{source}/{random.randint(1000,9999)}",
                theme,
                random.randint(1, 5),
                "No intent mentioned",
                f"User feedback regarding {theme}",
                now.isoformat()
            ))
            total_injected += 1
            
    conn.commit()
    conn.close()
    
    print(f"Successfully injected {total_injected} fully tagged reviews across App Store, Reddit, and YouTube.")

if __name__ == '__main__':
    run()
