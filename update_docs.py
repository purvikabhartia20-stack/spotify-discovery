import os

# Update 00_MASTER_README.md
readme = '00_MASTER_README.md'
if os.path.exists(readme):
    with open(readme, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove manual social media part
    content = content.replace('For Twitter, Instagram, and other sociak media platforms I will manually collect posts into a spreadsheet and upload it through the app. The app must support this upload as a normal feature.', 'Twitter and Instagram will be scraped automatically using API-free libraries (ntscraper and instaloader).')
    content = content.replace('### Source 5: Manual social media uploads (my responsibility, not scraped)\n- I will collect Twitter, Instagram, TikTok posts/comments manually into a CSV file\n- **Required CSV columns:** source (twitter/instagram/tiktok), date (YYYY-MM-DD), text, link, optional_handle\n- The app must have a file upload feature that accepts this CSV and adds rows to the main database', '### Source 5: Instagram and Twitter\n- **Libraries:** instaloader (Instagram), ntscraper (Twitter)\n- **Volume:** Top 50 posts each.\n- **Fields needed:** date, post text, link')

    with open(readme, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated 00_MASTER_README.md')

# Update Phase 2
p2 = 'docs/phase2_scrapers.md'
if os.path.exists(p2):
    with open(p2, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('four sources', 'six sources')
    content = content.replace('four small "robot collectors" — one each for Google Play Store, Apple App Store, Reddit, and YouTube.', 'six small "robot collectors" — one each for Google Play Store, Apple App Store, Reddit, YouTube, Instagram, and Twitter.')
    content = content.replace('Four scraper files exist', 'Six scraper files exist')
    content = content.replace('Same for the other three: scrape_appstore.py, scrape_reddit.py, scrape_youtube.py', 'Same for the others: scrape_appstore.py, scrape_reddit.py, scrape_youtube.py, scrape_instagram.py, scrape_twitter.py')

    if 'scrape_instagram' not in content:
        content = content.replace('### Shared helper', '### Instagram scraper\nUses instaloader to fetch posts without API keys.\n\n### Twitter scraper\nUses ntscraper to fetch tweets without API keys.\n\n### Shared helper')

    content = content.replace('playstore, appstore, reddit, youtube', 'playstore, appstore, reddit, youtube, instagram, twitter')

    with open(p2, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated phase2_scrapers.md')

# Update Phase 3
p3 = 'docs/phase3_tagger.md'
if os.path.exists(p3):
    with open(p3, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Token-Saving Strategy' not in content:
        content = content.replace('3. **Group them into batches of 20**', '3. **Apply Token-Saving Strategy:** Truncate all review text to a maximum of 150 characters (or 800 for YouTube transcripts) before sending to Gemini to save tokens.\n4. **Group them into batches of 20**')
        content = content.replace('4. **For each batch:**', '5. **For each batch:**')

    with open(p3, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated phase3_tagger.md')

# Update Phase 5
p5 = 'docs/phase5_backend.md'
if os.path.exists(p5):
    with open(p5, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('runs the four scrapers sequentially', 'runs the six scrapers sequentially')
    content = content.replace('scrape_playstore.run()\n   scrape_appstore.run()\n   scrape_reddit.run()\n   scrape_youtube.run()', 'scrape_playstore.run()\n   scrape_appstore.run()\n   scrape_reddit.run()\n   scrape_youtube.run()\n   scrape_instagram.run()\n   scrape_twitter.run()')

    with open(p5, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated phase5_backend.md')

# Update Phase 6
p6 = 'docs/phase6_frontend.md'
if os.path.exists(p6):
    with open(p6, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('Upload CSV: A file uploader for social media data (Twitter/Insta/TikTok)', 'Data sources: Shows stats for all six automatically scraped sources')
    content = content.replace('- I can upload a dummy CSV of social media posts, and they appear in the database', '- The dashboard correctly shows Instagram and Twitter data pulled by the scrapers')

    with open(p6, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated phase6_frontend.md')
