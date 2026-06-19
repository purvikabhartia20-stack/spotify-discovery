# Phase 3 — Tagger: Letting AI read every review and label it

## Goal

We have thousands of reviews sitting in the database, but they're just raw text — useless until someone reads them and decides what each one is about. That "someone" is Gemini AI. In this phase, we build a robot that picks up each review, sends it to Gemini with a very specific question, and saves Gemini's answer back into the database. Each review gets six labels: what it's about, whether it's positive or negative, what kind of user wrote it, how serious the complaint is, what they were trying to do, and a one-line summary. **At the end of this phase, every review in our database has these six labels filled in.**

Think of it like hiring a research assistant who reads each user review and writes you a sticky note: "This person is frustrated because Discover Weekly keeps showing the same artist." Now instead of reading thousands of reviews, you can read sticky notes and group them.

---

## What you'll see when Phase 3 is done

- A file `agents/tag_reviews.py` exists
- A file `prompts/tag_prompt.txt` exists with the exact instructions sent to Gemini
- Running `python agents/tag_reviews.py` processes every untagged review in the database
- Live progress: "Tagged 50/3,000... 100/3,000..."
- After it finishes, every review row has values in the theme, sentiment, segment, pain_severity, behavior_intent, and summary columns
- A small report at the end shows: total tagged, total failed, estimated API cost (should be near zero on free tier)
- I can manually inspect 30 random tagged reviews and confirm the labels make sense

---

## Files created or modified

| File | What it does |
|------|--------------|
| `agents/tag_reviews.py` | The main tagging script that loops through untagged rows |
| `prompts/tag_prompt.txt` | The exact prompt template sent to Gemini for each review |
| `agents/_common.py` | Updated with Gemini API helper functions |
| `data/reviews.db` | All reviews now have tags filled in |
| `data/runs.log` | Logs of tagging progress and any failures |

---

## Step-by-step plan

1. **Load the prompt template** from prompts/tag_prompt.txt
2. **Query the database** for all reviews where `tagged_at` is NULL (untagged)
3. **Group them into batches of 20** (one batch = one Gemini API call — much cheaper than calling per review)
4. **For each batch:**
   - Insert the 20 reviews into the prompt
   - Send to Gemini 2.5 Flash (fast and free-tier-friendly)
   - Wait for response
   - Parse the JSON response (a list of 20 tag objects)
   - For each tag object, save its 6 fields to the matching review in the database
   - Mark `tagged_at` with current timestamp
5. **Handle bad responses gracefully:**
   - If Gemini returns invalid JSON → retry once with stricter "return ONLY valid JSON" instruction
   - If still invalid → skip those 20 reviews, log them for manual review, continue
6. **Print live progress** every batch: "Tagged 240/3,200..."
7. **Track costs** — log estimated tokens used (free tier limit is generous, but we want visibility)
8. **At the end**, print summary: total tagged, total failed, retry count, estimated total tokens

---

## The exact tag prompt (this is the brain of the system)

Inside `prompts/tag_prompt.txt`, Antigravity writes this:

```
You are analyzing user reviews of Spotify to help a Product Manager understand music discovery problems. For each review below, return a structured JSON object.

Output format — return a JSON array with one object per review, in the same order:
[
  {
    "review_id": <integer matching input>,
    "theme": "<one of: discovery_difficulty, recommendation_quality, repeat_play_loop, search_problems, mood_matching, onboarding_issues, playlist_issues, audio_quality, pricing, ads, other>",
    "sentiment": "<one of: positive, neutral, negative, mixed>",
    "segment": "<one of: casual_listener, power_user, genre_specific, new_user, returning_user, unclear>",
    "pain_severity": <integer 1 to 5, where 1=minor annoyance, 5=app-breaking>,
    "behavior_intent": "<one short phrase describing what the user is trying to achieve, e.g. 'find new artists in my genre', 'wind down for sleep', 'discover music for road trips'>",
    "summary": "<one sentence summarizing the user's core point in your own words>"
  }
]

Rules:
- If a review is not in English, translate mentally and tag it the same way
- If a review is spam or off-topic (e.g. crypto promo), set theme to "other" and pain_severity to 1
- "discovery_difficulty" = user CAN'T find new music they like
- "recommendation_quality" = recommendations exist but are bad/wrong
- "repeat_play_loop" = same songs/artists keep coming back
- A 5-star review praising discovery is sentiment=positive but theme can still be "discovery_difficulty" if they're saying it's fixed
- If unsure about segment, use "unclear" rather than guessing wrong
- Be precise. A vague "this app sucks" without specifics → theme="other", behavior_intent="general dissatisfaction"

Reviews to tag:
[Antigravity inserts the 20 reviews here as JSON with their IDs]

Return ONLY the JSON array. No preamble, no markdown code fences, just raw JSON starting with [ and ending with ].
```

---

## Edge cases to handle

- **Gemini returns markdown-wrapped JSON** (```json ... ```) → strip the wrapper before parsing
- **Gemini returns fewer than 20 objects** → match by review_id, don't assume order
- **Gemini hallucinates a new label not in our list** (e.g. "music_quality" instead of "audio_quality") → log it, save it anyway, we'll clean up in Phase 4
- **API rate limit hit** → wait 60 seconds, retry the same batch
- **API quota fully exhausted** → save progress, exit cleanly with message: "Daily Gemini quota hit. Run this again tomorrow to continue."
- **Review text is empty after cleaning** → skip, mark as "skipped_empty" in tagged_at
- **Review is in a non-English script the model handles poorly** → save Gemini's attempt, flag for sample review later
- **Batch contains a review that breaks Gemini's safety filters** (rare, but possible if review mentions illegal content) → retry that one review alone with a placeholder tag if still rejected
- **Network drops mid-batch** → the batch is atomic; either all 20 save or none. Retry on reconnect.
- **JSON parsing fails twice in a row** → log the entire raw Gemini output to `data/failed_batches/` for manual debugging

---

## Validation checklist (for me to tick off before approving Phase 3)

- [ ] Every review in the database has a non-null `tagged_at` value (or is in the skipped log)
- [ ] I open 30 random tagged reviews and read them — at least 27/30 tags look correct to me
- [ ] No theme values are outside the allowed list (run a quick check)
- [ ] No pain_severity values are outside 1-5 range
- [ ] The total Gemini cost reported is near zero or zero (free tier)
- [ ] The failed_batches folder is either empty or contains less than 5% of total batches
- [ ] If I run the tagger again, it processes ZERO reviews (because they're all already tagged) — this confirms idempotency

---

## What I need to do BEFORE Phase 3 starts

Nothing technical. Just be ready to spend 15 minutes after Phase 3 finishes manually checking 30 sample tags. This is critical — if tagging accuracy is low, every later phase suffers.

If accuracy looks weak (less than 85% of my 30 samples are right), Antigravity refines the prompt and retags everything. This is normal and expected — accept the cost of one re-tag.

---

## If something breaks in Phase 3 — top 3 likely errors

### Error 1: "Gemini returned invalid JSON" appears repeatedly
**Why:** Gemini sometimes wraps responses in markdown code fences or adds explanatory text.
**Fix:** Strengthen the prompt's "return ONLY raw JSON" instruction, OR add a JSON cleaning function that strips markdown before parsing. Antigravity handles this in one prompt.

### Error 2: "RESOURCE_EXHAUSTED" or daily quota error
**Why:** Free Gemini API tier has daily limits (1500 requests/day on Flash as of 2026).
**Fix:** Tagging 3,000 reviews in batches of 20 = 150 requests, well within limit. If you hit this, check if other apps are using the same key. If not, wait 24 hours for reset.

### Error 3: Some tags look wrong on inspection
**Why:** Prompt isn't specific enough for edge cases.
**Fix:** Tell Antigravity which examples were wrong and how. It refines the prompt with examples (called "few-shot prompting"). Re-run tagging on failed reviews only.

---

## How much of my Antigravity credit this uses

Moderate. The script itself is simple (~150 lines), but tuning the prompt may need 2-3 iterations. Estimated agent requests: 10-20.

Note: This phase ALSO uses Gemini API requests directly (not Antigravity credits). Estimated Gemini Flash usage: 150 requests for full corpus. Well within free tier.

---

## Why Gemini Flash, not Pro, for this step

Gemini 2.5 Flash is faster, has higher free-tier rate limits, and is plenty smart for structured classification. We save Gemini 2.5 Pro (the deeper, slower model) for Phase 4 where we need real reasoning across thousands of reviews. This split keeps us well inside free tier on both models.

---

*End of Phase 3 document. Approve this — and verify 30 sample tags — before we move to Phase 4 (the synthesizer).*
