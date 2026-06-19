import sys
import yaml
import os

def check_python_version():
    if sys.version_info < (3, 11):
        print("❌ Python version is wrong. This project requires Python 3.11 or higher.")
        sys.exit(1)
    else:
        print(f"✅ Python version is {sys.version.split()[0]} (requires >= 3.11)")

def check_database():
    if os.path.exists('data/reviews.db'):
        print("✅ Database exists at data/reviews.db")
    else:
        print("❌ Database file not found at data/reviews.db")

def verify_setup():
    print("Verifying setup...\n")
    check_python_version()
    check_database()
    
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("❌ config.yaml file not found. Please create one based on the template.")
        return

    # Check Reddit
    user_agent = config.get('reddit', {}).get('user_agent', 'python:spotify-discovery-engine:v1.0')
    try:
        import requests
        headers = {"User-Agent": user_agent}
        response = requests.get("https://www.reddit.com/r/spotify/hot.json?limit=1", headers=headers)
        response.raise_for_status()
        print("✅ Reddit connection successful (JSON endpoint)")
    except Exception as e:
        print(f"❌ Reddit connection failed: {e}")

    # Check YouTube (yt-dlp)
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({"skip_download": True, "quiet": True}) as ydl:
            # We use a highly reliable public video ID for testing (Me at the zoo)
            ydl.extract_info("https://youtube.com/watch?v=jNQXAC9IVRw", download=False)
            print("✅ YouTube connection successful (yt-dlp)")
    except Exception as e:
        print(f"❌ YouTube connection failed: {e}")

    # Check Gemini
    gemini_api_key = config.get('gemini', {}).get('api_key')
    if gemini_api_key == 'YOUR_GEMINI_API_KEY' or not gemini_api_key:
        print("❌ Gemini api_key still has placeholder text — please replace it.")
    else:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content("Say hello")
            print("✅ Gemini connection successful")
        except Exception as e:
            print(f"❌ Gemini connection failed: {e}")

if __name__ == "__main__":
    verify_setup()
