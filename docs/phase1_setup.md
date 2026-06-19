# Phase 1 — Setup: Get the environment and keys ready

## Goal

Before we build anything, we need to make sure the laptop has everything required: Python installed, all the small free tools (libraries) installed, and one API key saved in a safe place. We also create the empty database file that will eventually hold all reviews. **No reviews are pulled in this phase. No analysis happens. We are just preparing the kitchen before we cook.**

Think of this like setting up a new desk on day one of a job: laptop, login credentials, notebook, pens. We're not doing real work yet. We're getting ready to do real work.

---

## What you'll see when Phase 1 is done

- A folder called `spotify-discovery/` exists on the laptop with the right structure
- A file called `config.yaml` exists with your one API key filled in
- A command called `python verify_setup.py` runs and prints "✅ All systems ready" with no errors
- An empty database file `data/reviews.db` exists with all the right empty tables created
- A `requirements.txt` file lists every library this project needs

If all five things are true, Phase 1 is complete.

---

## Files created or modified

| File | What it does |
|------|--------------|
| `config.yaml` | Stores your one API key safely (Gemini) |
| `requirements.txt` | Lists every Python library to install |
| `verify_setup.py` | A small check script that tests each connection |
| `data/reviews.db` | Empty SQLite database with table structure created |
| `data/runs.log` | Empty log file that will track every refresh later |
| `.gitignore` | Tells the project to never share secret keys publicly |
| `README.md` | A short user-facing readme separate from the master document |

---

## Step-by-step plan (what Antigravity will do)

1. **Create the folder structure.** Build empty folders: `agents/`, `data/`, `data/social_uploads/`, `reports/`, `prompts/`, `docs/`.
2. **Write requirements.txt** listing all libraries: google-play-scraper, app-store-scraper, requests, yt-dlp, youtube-transcript-api, instaloader, ntscraper, google-generativeai, streamlit, plotly, pandas, pyyaml, beautifulsoup4.
3. **Install all libraries** with one command (`pip install -r requirements.txt`).
4. **Create config.yaml template** with empty slots for the one API key. Add comments explaining where each key comes from.
5. **Create the database** — open SQLite, create a `reviews` table with all the columns we'll need (id, source, country, date, rating, text, url, scraped_at, theme, sentiment, segment, pain_severity, behavior_intent, summary, tagged_at). Also create a `runs` table to track each refresh. Also create a `sources` table to remember the last_scraped_at timestamp per source.
6. **Write verify_setup.py** — a small script that loads each API key and makes a tiny test call (1 Reddit post, 1 Gemini request, 1 YouTube search). It prints clear ✅ or ❌ for each connection.
7. **Tell me to fill in the one API key.** Pause and wait.
8. **After I confirm keys are filled in,** run verify_setup.py to confirm everything works.

---

## Edge cases to handle

- **Python version is wrong** → script checks for Python 3.11+ at the start and exits with a clear message if older.
- **pip install fails for one library** → continue trying the rest, then report which failed and a likely fix (usually upgrading pip).
- **Gemini API key returns 403** → tell me to check if the key is for AI Studio specifically, not Vertex AI.
- **Database file can't be created** → check if folder permissions are an issue, suggest moving the project out of system folders.
- **Internet is offline** → all three test calls fail at once → tell me to check internet, not API keys.

---

## Validation checklist (for me to tick off before approving Phase 1)

- [ ] I can see the folder `spotify-discovery/` on my laptop with the right subfolders inside
- [ ] `config.yaml` opens in a text editor and has my real keys (not placeholder text)
- [ ] Running `python verify_setup.py` prints all four ✅ marks (Gemini, Database)
- [ ] `data/reviews.db` exists and is not empty (you can check with any SQLite viewer, but I trust the verify script)
- [ ] `requirements.txt` exists and lists the libraries
- [ ] No error messages appeared during install

---

## What I need to do BEFORE Phase 1 starts

Get these one free API key. Each takes 5 minutes max. Save them in a temporary doc — I'll paste them into config.yaml when Antigravity asks.

### Key 3: Gemini API (one key)
1. Go to **aistudio.google.com**
2. Sign in with your Google account (same one as your Gemini Pro subscription)
3. On the left sidebar, click "Get API key"
4. Click "Create API key in new project"
5. Copy the key

That's it. Total time: 15 minutes if it's your first time, 5 minutes if you've done it before.

---

## If something breaks in Phase 1 — top 3 likely errors

**Why:** A library failed to install.
**Fix:** Run `pip install --upgrade pip` first, then `pip install -r requirements.txt` again. If still failing, tell Antigravity which library and it'll handle the specific case.

### Error 2: Reddit verify call returns "401 Unauthorized"
**Why:** Either the credentials are wrong, or you chose the wrong app type.
- **Setup needed:** None (using unauthenticated JSON endpoints)

### Error 3: Gemini returns "API key not valid"
**Why:** Either the key is from Vertex AI instead of AI Studio, or your account doesn't have access to the model.
**Fix:** Go to aistudio.google.com and generate a new key from there specifically. The keys from console.cloud.google.com are different and will not work for the Gemini API call we use.

---

## How much of my Antigravity credit this uses

This phase is mostly file creation and one small test script. Estimated agent requests: 5-8. This is the cheapest phase of the entire project.

---

*End of Phase 1 document. Approve this and we move to Phase 2 (the scrapers).*
