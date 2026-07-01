import sqlite3
import datetime
import random
from agents._common import save_reviews

def run():
    print("Injecting mock data for Apple, Reddit, and Social...")
    
    now = datetime.datetime.now()
    
    mock_reviews = [
        {
            'source': 'appstore',
            'country': 'US',
            'date': (now - datetime.timedelta(days=2)).isoformat(),
            'rating': 2,
            'text': "Spotify algorithm is broken on iOS. Discover Weekly keeps playing the same 5 songs. Also the app crashes when I open lyrics.",
            'url': None
        },
        {
            'source': 'appstore',
            'country': 'GB',
            'date': (now - datetime.timedelta(days=5)).isoformat(),
            'rating': 4,
            'text': "Love the app but the recommendations are getting stale. I miss when it actually found new indie artists for me.",
            'url': None
        },
        {
            'source': 'appstore',
            'country': 'DE',
            'date': (now - datetime.timedelta(days=1)).isoformat(),
            'rating': 1,
            'text': "Too many ads on the free tier, and the playlist suggestions don't even match my taste anymore.",
            'url': None
        },
        {
            'source': 'reddit',
            'country': None,
            'date': (now - datetime.timedelta(days=3)).isoformat(),
            'rating': 150,
            'text': "Anyone else feel like Release Radar is just pushing label-sponsored tracks now? It's not actually tailored to my listening history at all.",
            'url': "https://reddit.com/r/spotify/1"
        },
        {
            'source': 'reddit',
            'country': None,
            'date': (now - datetime.timedelta(days=10)).isoformat(),
            'rating': 45,
            'text': "How do I reset my algorithm? I listened to white noise for one night and now my entire Discover Weekly is ruined. I need a reset button.",
            'url': "https://reddit.com/r/truespotify/2"
        },
        {
            'source': 'reddit',
            'country': None,
            'date': (now - datetime.timedelta(days=12)).isoformat(),
            'rating': 89,
            'text': "Autoplay is driving me insane. No matter what radio station I start, within 10 songs it reverts back to the same 20 songs I always listen to.",
            'url': "https://reddit.com/r/Music/3"
        },
        {
            'source': 'youtube',
            'country': None,
            'date': (now - datetime.timedelta(days=4)).isoformat(),
            'rating': 0,
            'text': "Spotify's new UI update makes it so hard to find new music. The TikTok style feed is terrible for actually discovering full albums.",
            'url': "https://youtube.com/watch?v=1"
        },
        {
            'source': 'youtube',
            'country': None,
            'date': (now - datetime.timedelta(days=7)).isoformat(),
            'rating': 0,
            'text': "Apple Music genuinely has better recommendations now. Spotify's algorithm is too focused on keeping you engaged with what you already know.",
            'url': "https://youtube.com/watch?v=2"
        }
    ]
    
    new_count = save_reviews(mock_reviews)
    print(f"Injected {new_count} mock records.")
    
if __name__ == '__main__':
    run()
