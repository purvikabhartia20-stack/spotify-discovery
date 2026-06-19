# Spotify Discovery Engine — Master README

> **For the AI assistant reading this:** This is the complete project brief. Read it fully before doing anything. After reading, your first task is to create 8 separate phase documents (phase1.md through phase8.md) inside a /docs folder. Do NOT start writing code until I explicitly say "Begin Phase 1." Wait for my approval after each phase before starting the next.

---

## 1. What we are building, in plain language

I am a Product Manager on the Growth team at Spotify. My goal is to figure out **why users don't discover new music** and **why they keep listening to the same songs**. To answer this, I need to read thousands of reviews and complaints from real Spotify users.

Reading them all by hand is impossible. So I'm building a small web app on my own laptop. The app does five things:

1. **Goes out to the internet** and grabs Spotify reviews from four places: Google Play Store, Apple App Store, Reddit, and YouTube comments.
2. **Reads every single review** using an AI (Gemini) and writes a little tag on each one — what topic it's about, whether it's happy or angry, what kind of user wrote it, how serious the complaint is.
3. **Lets me upload extra reviews** from social media (Twitter, Instagram, TikTok) as a spreadsheet, since those sites don't let us grab data automatically.
4. **Generates a report** that answers questions about music discovery, using actual quotes from real users as proof.
5. **Shows everything in a website I can open on my laptop** — with charts, a refresh button, the report, and a chat box where I can ask relevant questions and get answers from my own data.

That's the whole product.

---

## 2. Who I am and what I know

- **I am NOT a coder.** I cannot write code, debug code, or read code in detail. I can read plain English explanations of what code does.
- I am a Product Manager. I understand product thinking, user segments, feature prioritization.
- I will be running Antigravity/ or any other IDE as my AI coding partner. I expectit to write all code, run it, fix errors itself, and explain in plain English what it did.
- When you (the AI) explain something to me, **explain it like I'm intelligent but technical jargon doesn't help me.** Use analogies. Avoid words like "ORM", "async", "middleware" unless you also explain them.
- If something goes wrong, **explain WHY it went wrong before fixing it.** I'm trying to learn the system, not just get an output.

---

## 3. The six questions the project must answer

These are the actual PM questions. Every output of this project ultimately exists to answer these and more similar to these:

1. Why do users struggle to discover new music?
2. What are the most common frustrations with recommendations?
3. What listening behaviors are users trying to achieve?
4. What causes users to repeatedly listen to the same content?
5. Which user segments experience different discovery challenges?
6. What unmet needs emerge consistently across reviews?

---

## 4. Hard constraints — these CANNOT be broken

### Money
- **Everything must be free.** Zero dollars spent on anything.
- I have a Google Gemini Pro subscription (Google One AI Pro). Use this where it applies.
- I have Antigravity free tier access (upgraded slightly because of Gemini Pro).
- No paid APIs. No paid services. No "just $5/month" anything.

### Tools and AI engines allowed
- **Gemini API via Google AI Studio** (free tier, comes with my Pro subscription). This is the ONLY AI model used inside the app code. Use Gemini 2.5 Flash for bulk tagging (it's faster and cheaper on free tier), Gemini 2.5 Pro for final synthesis (better reasoning).

- **Free Python libraries only**: google-play-scraper, app-store-scraper, requests, yt-dlp, youtube-transcript-api, instaloader, ntscraper, streamlit, sqlite3 (built-in), plotly, pandas, pyyaml, beautifulsoup4. and any other if applicable

### Tools NOT allowed
- No paid AI APIs (OpenAI, Anthropic, Grok)
- No paid scraping services (Apify paid tier, ScraperAPI, etc.)
- No paid databases (Supabase paid, MongoDB Atlas paid)
- No paid hosting (only Streamlit Community Cloud free tier)
- No Twitter/X API (it costs $100/month)
- No TikTok API (locked down)
- No Instagram API (locked down)

### Where social media comes in
For Twitter, Instagram, and other sociak media platforms I will manually collect posts into a spreadsheet and upload it through the app. The app must support this upload as a normal feature.

### Tech stack — locked in, do not propose alternatives
- **Language:** Python 3.11+
- **UI framework:** Streamlit (because frontend and backend live in one file, simple for a non-coder)
- **Database:** SQLite (single file, no server needed)
- **Charts:** Plotly (works natively inside Streamlit)
- **AI:** Gemini API (Flash for bulk, Pro for synthesis)
- **Deployment:** Streamlit Community Cloud free tier OR just my local laptop

---

## 5. Data sources — exactly what to scrape and how

### Source 1: Google Play Store
- **Library:** google-play-scraper (free, no key needed)
- **Target:** Spotify app, package name `com.spotify.music`
- **Volume:** 2,000 most recent reviews
- **Countries:** US, UK, IN
- **Sort:** Newest first
- **Fields needed:** date, rating (1-5 stars), review text, username (anonymize), country code

### Source 2: Apple App Store
- **Library:** app-store-scraper (free, no key needed)
- **Target:** Spotify app, app ID `324684580`
- **Volume:** 500 reviews per country
- **Countries:** US, GB, IN

- **Fields needed:** date, rating, title, review text, country code

### Source 3: Reddit
- **Library:** requests (fetching public JSON endpoints directly without API credentials)
- **Setup needed:** None (using unauthenticated JSON endpoints)
- **Subreddits to search:** r/spotify, r/Music, r/truespotify, r/SpotifyThrowbacks, r/LetsTalkMusic
- **Search terms:** "discover weekly", "release radar", "recommendations", "algorithm", "for you", "daily mix", "music discovery"
- **Volume:** Top 50 posts per search term per subreddit (last 6 months) + top 15 comments on each post
- **Fields needed:** date, post title, post body, comment text, score (upvotes), subreddit name, permalink

### Source 4: YouTube comments
- **Library:** google-api-python-client (free, requires API key from Google Cloud Console)
- **Search queries:** "Spotify discover weekly review", "Spotify algorithm broken", "Spotify recommendations bad", "Spotify discovery feature", "Spotify vs Apple Music discovery"
- **Volume:** Top 20 videos per query + up to 100 top-level comments per video
- **Fields needed:** video title, video URL, date, comment text, like count, channel name

### Source 5: Manual social media uploads (my responsibility, not scraped)
- I will collect Twitter, Instagram, TikTok posts/comments manually into a CSV file
- **Required CSV columns:** source (twitter/instagram/tiktok), date (YYYY-MM-DD), text, link, optional_handle
- The app must have a file upload feature that accepts this CSV and adds rows to the main database

---

## 6. The 8 phases — overview

Build in this exact order. Do not skip ahead. Do not combine phases.

| Phase | Goal | Time | Deliverable |
|-------|------|------|-------------|
| 1 | Environment + API keys setup | 30 min | All connections verified working |
| 2 | Database schema + all scrapers | 60 min | reviews.db with 5,000+ rows |
| 3 | Tagger using Gemini API | 45 min | All reviews tagged with structured JSON |
| 4 | Synthesizer for 6 PM questions | 30 min | insight_report.md generated |
| 5 | Backend orchestration | 30 min | Single pipeline.py runs all steps in order |
| 6 | Streamlit frontend with 5 tabs | 45 min | Working app.py with UI |
| 7 | End-to-end testing + accuracy check | 30 min | Verified working, accuracy sampled |
| 8 | Deploy + polish + PDF export | 45 min | Live URL + PDF report ready for submission |

**Total estimated build time:** ~6 hours of Antigravity work, plus my approval time at each checkpoint.

---

## 7. The phase document protocol

After reading this README, your VERY FIRST task is to create 8 markdown files inside `/docs` these will be made only when I instruct you to make one by one, as i will attach a context image for each and every file as a reference, so dont rush and i will be uploading these one by one for you to read and understand, we will be working on the project according to these instructions.
- `/docs/phase1_setup.md`
- `/docs/phase2_scrapers.md`
- `/docs/phase3_tagger.md`
- `/docs/phase4_synthesizer.md`
- `/docs/phase5_backend.md`
- `/docs/phase6_frontend.md`
- `/docs/phase7_testing.md`
- `/docs/phase8_deploy.md`

**Each phase document MUST contain these sections:**

1. **Goal** — one paragraph in plain English: what we're building in this phase and why
2. **What you'll see when it's done** — concrete things I can verify (a file exists, a command works, etc.)
3. **Files created or modified** — full list with one-line purpose for each
4. **Step-by-step plan** — what the AI will do, in plain language, numbered
5. **Edge cases to handle** — every realistic thing that could go wrong, and what the code should do about it
6. **Validation checklist** — what I (the PM) need to verify before approving this phase
7. **What I need to do before this phase starts** — any API keys, decisions, manual setup
8. **If something breaks** — top 3 likely errors and how to fix each one
you'll get an understanding post reading the file  i provide while giving too


---

## 8. Edge cases that apply to EVERY phase

These are universal. Bake them into every phase's code:

1. **Network failures** — every external API call must retry 3 times with exponential backoff (wait 1s, 2s, 4s).
2. **Rate limits** — when hit, pause for the time specified in the response header. Never silently fail.
3. **Empty results** — if a scraper finds zero new reviews, log it clearly and continue. Don't crash.
4. **Encoding issues** — many reviews contain emojis, special characters, or non-Latin scripts. Use UTF-8 everywhere.
5. **Duplicate reviews** — same review pulled twice should be detected (by source+date+text hash) and skipped.
6. **Long reviews** — some reviews are huge. Truncate to 4,000 characters before sending to Gemini.
7. **API key missing** — if config.yaml lacks a key, show me a clear error: "Gemini API key missing in config.yaml. Get one at console.cloud.google.com." NOT a stack trace.
8. **Database locked** — SQLite can lock if accessed twice. Wrap writes in try/except, retry once.
9. **AI returns invalid JSON** — Gemini sometimes returns malformed JSON. Parse defensively. On failure, retry the single review with a stricter prompt. Skip after 2 failures and log.
10. **Slow runs** — the Refresh button can take 20+ minutes on first run. Show a live progress bar and step-by-step status messages so I know it's not frozen.

---

## 9. The success criteria for the whole project

I will consider the project done when ALL of these are true:

- I can run `streamlit run app.py` on my laptop and the app opens in my browser.
- The Dashboard tab shows charts with real data from real reviews.
- The Refresh button works and only pulls new reviews on subsequent runs.
- I can upload a social media CSV and the data appears in the database.
- The Insights tab shows a clear answer to each of the 6 PM questions with at least 3 real user quotes per question.
- The Q&A tab lets me ask free-form questions and answers come from the data.
- I can export the insight report as PDF.
- A README in the project root explains how to set up and run it.
- Each of the 8 phase documents accurately describes what was built.

---

## 10. Tone and explanation style for me

When you explain things to me:
- Use plain English. Pretend you're explaining to a smart PM friend over coffee.
- When you use a technical term, define it in brackets the first time: "We'll use SQLite (a small database that lives in one file, no server needed)."
- Show me what changed in human terms: "Created the scraper file. It pulls 2,000 reviews from Play Store. Tested it — it works."
- Don't dump code at me unless I ask. Instead, summarize what the code does.
- When you encounter an error, tell me: (1) what happened, (2) why, (3) what you're going to do about it.

---

## 11. Your first action right now

After reading this README, do exactly this and nothing more:

1. Create the `/docs` folder.
2. Reply to me with: "I've read the README " and i will be providing you the context images one by one for each file.
Do NOT create any other files. Do NOT write any code yet.

The phase documents themselves are the plan. We review them together before any code is written. That's how we avoid wasted credits and broken builds.