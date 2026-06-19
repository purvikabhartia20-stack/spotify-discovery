# Phase 5 — Backend: Wiring everything into one pipeline

## Goal

So far we have four scrapers, one tagger, and one synthesizer — six separate Python files that each do one thing. They work, but right now I'd have to run them one by one in the correct order, every single time, manually. That's not a real product. This phase ties them all together into one single "Refresh" button that, when pressed, runs everything in the right order, only pulls new data, handles social CSV uploads, and updates a log of what happened. **At the end of this phase, one command (`python pipeline.py`) runs the entire end-to-end process from scrape to report.**

Think of it like a factory assembly line. We've built each station individually. Now we connect them with conveyor belts, add a master ON switch, and add quality checks between stations.

---

## What you'll see when Phase 5 is done

- A file `pipeline.py` exists at the project root
- A file `agents/merge_social.py` exists for handling social CSV uploads
- Running `python pipeline.py` executes scrape → tag → synthesize in order
- Live progress shown: "[1/6] Scraping Play Store... done. [2/6] Scraping App Store... done." etc.
- A new entry appears in `data/runs.log` after each run with timestamps and counts
- If I run pipeline.py a second time within an hour, it pulls almost nothing (because data is already fresh)
- A command `python pipeline.py --upload-social path/to/file.csv` merges social media uploads into the database before tagging

---

## Files created or modified

| File | What it does |
|------|--------------|
| `pipeline.py` | The master script — runs everything in order |
| `agents/merge_social.py` | Reads a CSV upload and adds rows to the database |
| `agents/_common.py` | Updated with orchestration helpers |
| `data/runs.log` | Now structured: each run has a timestamp, source counts, errors, duration |

---

## Step-by-step plan

### What pipeline.py does, in order

1. **Print a banner** with timestamp and version
2. **Check config.yaml exists** — fail fast with friendly message if not
3. **Open a "run" entry** in runs.log with start_time
4. **Step 1: Run scrape_playstore.py** — capture how many new reviews were added
5. **Step 2: Run scrape_appstore.py** — same
6. **Step 3: Run scrape_reddit.py** — same
7. **Step 4: Run scrape_youtube.py** — same
8. **Step 5: Process pending social CSV uploads** if any are in data/social_uploads/
9. **Step 6: Run tag_reviews.py** — only on untagged rows (incremental)
10. **Step 7: Run synthesize.py** — generates a fresh report
11. **Close the run entry** in runs.log with end_time, total duration, total new reviews, total tagged, error count
12. **Print a final summary**: "✅ Refresh complete. 47 new reviews, 47 tagged, report saved to reports/insight_2026-06-18.md"

### What merge_social.py does

1. Accept a CSV file path as argument
2. Validate the CSV has the required columns: source, date, text, link
3. For each row, check if it's already in the database (by hash)
4. If new, insert into the reviews table with source="social_<platform>"
5. Mark tagged_at as NULL so the tagger picks them up next run
6. Move the processed CSV into `data/social_uploads/processed/` so it doesn't re-process
7. Print: "Added 234 new social posts to the corpus"

---

## Edge cases to handle

### Pipeline orchestration
- **One step fails** → log it, but continue to next step. Don't let a failed YouTube scrape prevent the report from being generated.
- **All scrapers fail** (e.g. internet is down) → skip tagging and synthesis (nothing new to tag), log "no new data, skipping analysis"
- **Tagger is interrupted mid-run** → next pipeline run resumes from where it stopped (because untagged rows are still untagged)
- **Synthesizer fails** → previous report still exists, log the failure, exit code 1
- **Pipeline runs while another pipeline is already running** → detect via lockfile, refuse with "Another pipeline run is in progress."
- **Disk space low** → check at start, warn if less than 500MB free
- **runs.log gets very long over months** → rotate it (keep last 100 runs in main file, archive older)

### Social CSV merger
- **CSV is malformed** (missing columns, wrong types) → reject with line-by-line error report, don't insert anything
- **CSV has 10,000 rows** → process in chunks of 500 to avoid memory issues
- **CSV has duplicate rows within itself** → dedupe before inserting
- **A row has empty text** → skip that row, log it
- **CSV uses different date format than expected** (ISO vs US vs UK) → try to parse multiple formats, fall back to today's date with a warning
- **Social CSV row has a date in the future** → flag as suspicious, save anyway
- **CSV is just an Excel export saved as CSV** with weird encoding → handle BOM and various encodings (utf-8, utf-8-sig, latin-1)

---

## Validation checklist (for me to tick off before approving Phase 5)

- [ ] `python pipeline.py` runs end-to-end without crashing
- [ ] A run entry appears in runs.log with all expected fields
- [ ] Running it again within 1 hour shows "no new data" for each scraper
- [ ] Uploading a small test CSV with 5 rows adds 5 rows to the database
- [ ] Re-uploading the same CSV results in 0 new rows (dedup works)
- [ ] The pipeline can be Ctrl+C'd mid-run and the next run resumes correctly
- [ ] The final summary message at the end is clear and useful
- [ ] If I delete the Gemini API key from config, the pipeline still completes other steps and reports YouTube as failed

---

## What I need to do BEFORE Phase 5 starts

Optionally: create a small test CSV with 5 fake social media rows. I'll use it to validate the upload feature.

Example test_social.csv:
```
source,date,text,link
twitter,2026-06-15,"Spotify keeps showing me the same 5 artists in Discover Weekly. So annoying.",https://twitter.com/example/1
instagram,2026-06-14,"Why is Discover Weekly so bad now? It used to be magic.",https://instagram.com/example/2
tiktok,2026-06-12,"My Discover Weekly is literally just my Liked Songs played back to me",https://tiktok.com/example/3
twitter,2026-06-10,"Apple Music's For You beats Spotify's algorithm tbh",https://twitter.com/example/4
twitter,2026-06-08,"Release Radar finally added a track I love!! Thanks Spotify",https://twitter.com/example/5
```

---

## If something breaks in Phase 5 — top 3 likely errors

### Error 1: "Database is locked" repeatedly
**Why:** SQLite doesn't handle concurrent writes well. If two parts of the pipeline try to write at once, one waits or errors.
**Fix:** Antigravity should already serialize writes. If still happening, add a retry-with-backoff wrapper around all database writes. This is a one-line fix.

### Error 2: Pipeline runs but produces empty report
**Why:** No new data was scraped (already up to date) AND no social CSV was uploaded, so nothing new to synthesize. The previous report is still valid.
**Fix:** Show a clearer message: "Database has 8,247 reviews (0 new this run). Existing report at reports/insight_2026-06-17.md is still current. To regenerate anyway, run with --force-resynthesize."

### Error 3: Social CSV upload says "rejected" with no detail
**Why:** CSV header doesn't match expected columns exactly.
**Fix:** The error message should show me what columns it expected vs what it found, side by side. Antigravity adds this detail.

---

## How much of my Antigravity credit this uses

Light to moderate. The pipeline is mostly glue code. Estimated agent requests: 8-12.

---

## What this phase enables

After Phase 5 is done, the system is functionally complete from a backend perspective. Everything works from the command line. The only thing missing is a friendly user interface — which is exactly what Phase 6 builds.

Importantly, Phase 5's pipeline.py is what the Streamlit Refresh button will call in Phase 6. So if pipeline.py works perfectly here, Phase 6 becomes much simpler.

---

*End of Phase 5 document. Approve and we move to Phase 6 (the Streamlit UI).*
