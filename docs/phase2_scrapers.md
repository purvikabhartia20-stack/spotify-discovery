# Phase 2 — Scrapers: Pulling reviews from six sources

## Goal

This is where we actually start collecting real Spotify reviews. We build six small "robot collectors" — one each for Google Play Store, Apple App Store, Reddit, YouTube, Instagram, and Twitter. Each one knows how to visit its source, grab reviews, clean them up, and save them into our database. **At the end of this phase, the database should have somewhere between 5,000 and 10,000 real Spotify reviews from real users**, ready to be analyzed by AI in Phase 3.

Think of it like sending out four interns to four different libraries with instructions to bring back specific kinds of books. Each intern has their own routine, their own challenges, and brings back their findings to the same central shelf.

---

## What you'll see when Phase 2 is done

- Five scraper files exist inside `agents/` folder
- Running `python agents/scrape_playstore.py` saves Play Store reviews into the database
- Same for the others: scrape_appstore.py, scrape_reddit.py, scrape_youtube.py
- A simple SQL query shows the total number of reviews per source.
- Manual CSV uploads cover Instagram and Twitter, processed securely via the dashboard.
- Each scraper logs its progress in plain English so I can see what's happening live

---

## Files created or modified

| File | What it does |
|------|--------------|
| `agents/scrape_playstore.py` | Pulls reviews from Google Play Store using google-play-scraper |
| `agents/scrape_appstore.py` | Pulls reviews directly from Apple's public iTunes RSS feed |
| `agents/scrape_reddit.py` | Pulls posts from Reddit via XML RSS endpoints to bypass rate limits |
| `agents/scrape_youtube.py` | Pulls comments using the official YouTube Data API v3 |
| `agents/_common.py` | Shared helper functions used by all scrapers (database connection, deduplication, logging) |
| `data/reviews.db` | Now contains real review data |
| `data/runs.log` | Updated with timestamps and counts from this run |

---

## Step-by-step plan (what each scraper does)

### Play Store scraper
1. Connect to google-play-scraper library
2. Request the Spotify app's reviews, sorted by newest
3. Loop through 4 countries: US, UK, India, Germany
4. For each country, pull up to 500 reviews
5. Clean each review: remove HTML, trim long text, keep emojis
6. Check if this review is already in our database (by hash)
7. If new, insert into the `reviews` table with all fields
8. Update the `sources` table with timestamp of latest review found
9. Print a progress message every 100 reviews

### App Store scraper
1. Fetch data directly from Apple's public iTunes RSS feed (bypassing restrictive scraping libraries).
2. Loop through countries (US, GB, CA, AU, IN).
3. Insert reviews into the database.

### Reddit scraper
1. Fetch data from Reddit using public XML RSS endpoints (`new.rss`) to completely bypass unauthenticated JSON rate-limiting (429 errors).
2. Target subreddits like r/spotify and r/truespotify.
3. Parse the XML, strip HTML, and save the genuine posts.

### YouTube scraper
1. Authenticate with the official Google API Client using the YouTube API key from `config.yaml`.
2. Search for videos matching queries like "Spotify discover weekly".
3. Fetch the top comments for those videos via the `commentThreads` endpoint.
4. Save the actual human comments into the database.

### Social Uploads (Instagram/Twitter)
Since Instagram and Twitter strictly block unauthenticated scraping from cloud networks, they are not handled by automated scripts. Instead, users manually export CSV data and upload it via the "Upload Social Data" tab in the Streamlit dashboard, which injects them directly into the database.

### Shared helper (_common.py)
- Database connection function (open, close safely)
- Deduplication function (hash check by source + date + first 200 chars of text)
- Logger function (write to runs.log with timestamp)
- Incremental check function (compare review date to last_scraped_at for this source — skip if older)

---

## Edge cases to handle

### Play Store specific
- **App not found in some country** → log it, continue to next country
- **Review text is None** → skip that review, don't crash
- **Review date is in unusual format** → use the library's parser, fall back to today's date if it fails

### App Store specific
- **App Store rate limit (HTTP 429)** → wait 60 seconds, retry
- **Some countries return empty** → log it, continue
- **Review title is empty but body is full** → use body, ignore title

### Reddit specific
- **Subreddit doesn't exist or is banned** → catch the error, log it, move to next subreddit
- **Post is deleted/removed** → skip its comments too
- **Comment is "[removed]" or "[deleted]"** → skip
- **Comment is from a bot (AutoModerator)** → skip
- **Hitting 100 queries/minute limit** → We will add manual delays to avoid this, log when it happens
- **Comment thread is massively nested** → only pull top-level comments and direct replies, ignore deeper threads

### YouTube specific
- **Comments are disabled on a video** → skip that video, log it
- **Daily quota of 10,000 units approaching** → save what we have, exit cleanly with a clear message: "YouTube daily quota nearly exhausted, resume tomorrow"
- **Comments are in many languages** → save as-is, language detection is Phase 3's job
- **Spam comments** → save them anyway, Gemini will filter in tagging

### Universal
- **Internet drops mid-scrape** → save what we have so far to database, log the error, exit cleanly
- **SQLite database is locked** by another process → wait 2 seconds, retry once
- **Same review appears in two countries** (same user, same date) → keep both, mark country code
- **Review is in non-English language** → save it. Gemini handles multilingual tagging in Phase 3.

---

## Validation checklist (for me to tick off before approving Phase 2)

- [ ] All four scrapers ran without crashing
- [ ] The total review count in the database is between 5,000 and 10,000
- [ ] I see roughly balanced counts: at least 1,000 from each major source
- [ ] When I look at 5 sample rows, they look like real Spotify complaints/praises (not gibberish or spam-only)
- [ ] The `runs.log` file shows clear progress and any errors that occurred
- [ ] If I run any scraper a SECOND time, it pulls zero new reviews (because they're already saved) — this confirms incremental logic works
- [ ] Reviews have proper UTF-8 text (emojis show correctly)

---

## What I need to do BEFORE Phase 2 starts

Nothing — assuming Phase 1 was approved. All keys are already in config.yaml.

Optionally: open `agents/scrape_playstore.py` in a text editor once Antigravity finishes writing it. You don't need to understand the code, but skim it. The comments should tell you what each section does in plain English.

---

## If something breaks in Phase 2 — top 3 likely errors

### Error 1: Reddit returns "received 429 HTTP response" repeatedly
**Why:** You're hitting the 100 requests/minute limit.
**Fix:** The script will back off automatically. If it's still happening, reduce the search terms or subreddits in scrape_reddit.py. Antigravity can do this — just say "reduce the Reddit scrape volume by half."

### Error 2: YouTube returns "quota exceeded"
**Why:** We are using yt-dlp which does not have strict API quotas, but may be rate-limited by IP. Each comment fetch costs 1 unit, each search costs 100 units.
**Fix:** Use proxies or wait for rate limits to reset. Antigravity can recalculate the math.

### Error 3: Play Store scraper returns empty
**Why:** Either the app ID is wrong (unlikely for Spotify) or your IP is being rate-limited by Google.
**Fix:** Add a small `time.sleep(2)` between country loops. Antigravity adds this with one prompt.

### Error 4 (bonus): App Store returns "503 Service Unavailable"
**Why:** Apple sometimes blocks rapid requests.
**Fix:** Spread the request across more time. The scraper should already have retries with exponential backoff. If persistent, wait 30 minutes and retry.

---

## How much of my Antigravity credit this uses

This is a moderate-cost phase. Four scrapers + one helper = ~5 files. Estimated agent requests: 15-25, depending on debugging. If everything works first try, much less.

---

## What gets stored in the database after Phase 2

Each review becomes one row with these columns:
- `id` — unique number
- `source` — one of: playstore, appstore, reddit, youtube, instagram, twitter
- `country` — country code where applicable
- `date` — when the review was posted
- `rating` — 1-5 stars (only for Play Store / App Store)
- `text` — the actual review content
- `url` — link back to the source if available
- `scraped_at` — when our scraper pulled it
- `theme`, `pain_severity`, `behavior_intent`, `summary` — all empty for now (Phase 3 fills these in)
- `tagged_at` — empty for now

The tagging columns existing now but empty is intentional — we don't need to change the schema in Phase 3, just populate.

---

*End of Phase 2 document. Approve this and we move to Phase 3 (the AI tagger).*
