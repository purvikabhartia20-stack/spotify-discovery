# Phase 4 — Synthesizer: Turning tagged reviews into PM-ready answers

## Goal

We now have thousands of tagged reviews — but tags alone don't answer a PM's questions. A PM doesn't want "1,247 reviews are about discovery_difficulty." A PM wants "Here's WHY users struggle to discover music, in three patterns, with quotes from real users." This phase builds the script that takes our entire tagged dataset and writes an actual PM-quality report answering each of the six questions from the assignment.

Think of it like hiring a senior analyst. You hand them a stack of 3,000 tagged sticky notes and say "by Monday, write me a memo answering these six questions with evidence." They group similar notes, find patterns, pick the best quotes, and write the memo. That's what this phase builds — except the analyst is Gemini 2.5 Pro and Monday is 5 minutes from now.

---

## What you'll see when Phase 4 is done

- A file `agents/synthesize.py` exists
- A file `prompts/synth_prompt.txt` exists with the synthesis instructions
- Running `python agents/synthesize.py` produces a Markdown file at `reports/insight_report_YYYY-MM-DD.md`
- The report has 6 clearly labeled sections — one per PM question
- Each section contains: 2-3 patterns identified, 3-5 verbatim user quotes per pattern
- The report ends with an "Unmet Needs" summary and "Recommended Next Steps" — both PM-style writing
- I can read the entire report in 10 minutes and understand the state of music discovery from real user voices

---

## Files created or modified

| File | What it does |
|------|--------------|
| `agents/synthesize.py` | Main synthesis script |
| `prompts/synth_prompt.txt` | Instructions sent to Gemini for the report |
| `reports/insight_report_YYYY-MM-DD.md` | The actual PM report |
| `reports/data_snapshot_YYYY-MM-DD.json` | A JSON summary of the data used (for reproducibility) |

---

## Step-by-step plan

1. **Pull aggregate data from the database** — counts per theme, top complaints by frequency, top complaints by severity
2. **Select representative quotes** — for each theme, pick 10-15 reviews that best exemplify the pattern (highest pain_severity within that theme, sorted by date for recency mix)
3. **Build six prompts**, one for each PM question, each containing:
   - The question
   - Relevant theme counts and percentages
   - 15-20 verbatim review quotes with metadata
4. **Send each prompt to Gemini 2.5 Pro** (not Flash — we want deeper reasoning here)
5. **Receive a structured Markdown answer** with patterns identified, quotes embedded, and PM-style framing
6. **Combine all 6 answers into a single Markdown file** with executive summary at top
7. **Add a final section** that asks Gemini to identify cross-cutting "Unmet Needs" by reading the 6 previous answers
8. **Save the final report** to reports/ with today's date in filename
9. **Also save a JSON snapshot** of the underlying data (counts, top quotes) so the report is reproducible

---

## The synthesis prompt structure (one per PM question)

Inside `prompts/synth_prompt.txt`, Antigravity writes a template like this:

```
You are a senior product analyst writing a memo for a Spotify Growth PM about music discovery problems. Below is data from analyzing thousands of real user reviews.

THE QUESTION:
[insert one of the 6 PM questions]

DATA SUMMARY:
- Total reviews analyzed: [number]
- Top themes related to this question: [data with frequencies]
- Severity distribution: [data]

VERBATIM USER REVIEWS (15 selected):
[20 quotes with metadata: source, date, pain_severity]

YOUR TASK:
Write a structured answer (300-500 words) with:

1. **Top-line finding** (one bold sentence — the headline insight)

2. **Three patterns** — concrete sub-themes with evidence
   - Pattern name
   - What it means in user terms
   - 2-3 verbatim quotes as evidence (use real review text, attribute by source: "Play Store review, May 2026, casual_listener")
   - How widespread it is (rough %)

3. **One concrete implication** — what this means for product decisions

Style:
- Plain English, no jargon
- Quotes in italics
- Specific, not vague ("28% of casual listeners" not "many users")
- No fluff, no hedging
- Don't repeat the question

Output as clean Markdown.
```

---

## Edge cases to handle

- **Some PM questions overlap** (question 1 and 2 both touch recommendations) → that's fine, the synthesizer can repeat insights across answers if relevant. Don't try to deduplicate.
- **A theme has too few reviews to draw conclusions** (less than 30 tagged) → the answer should say so explicitly, not invent confidence
- **Quotes contain profanity or slurs** → keep them as-is for authenticity, but warn me in a small footer that they're verbatim
- **Quotes contain personal info** (usernames, phone numbers) → strip with regex before sending to Gemini
- **Report becomes massive** → 6 questions × 500 words = ~3,000 words plus quotes ≈ 5,000 words total. That's fine for a PM doc.
- **Gemini Pro returns answer in wrong format** → retry with stricter instructions
- **Quotes are too long to include in full** → truncate to first 200 chars with "..."
- **Two patterns describe the same thing slightly differently** → that's a Gemini judgment call; accept it, I can edit later
- **A question has no clear answer in the data** → the synthesizer says so honestly: "Insufficient signal in current data. Recommend collecting more reviews in [area]."

---

## Validation checklist (for me to tick off before approving Phase 4)

- [ ] The report file exists in reports/ folder with today's date
- [ ] Each of the 6 PM questions has its own labeled section
- [ ] Each section has at least 5 verbatim user quotes
- [ ] The quotes look like real Spotify users, not generic
- [ ] The patterns identified actually make sense as PM insights, not just topic labels
- [ ] The "Unmet Needs" section synthesizes across all 6 — not just a list

- [ ] Total report length is between 3,000 and 6,000 words (any less = thin, any more = unreadable)
- [ ] I can confidently present this report to a Spotify Growth PM and they'd find it useful

---

## What I need to do BEFORE Phase 4 starts

Read your assignment brief one more time. Confirm the 6 PM questions in master README are exactly the ones the assignment asks. If your assignment has slightly different wording, tell Antigravity to update prompts/synth_prompt.txt before running.

This phase is the one where the project's output quality is most visible. Spend extra time on validation.

---

## If something breaks in Phase 4 — top 3 likely errors

### Error 1: Report is too generic, sounds like ChatGPT marketing copy
**Why:** The prompt isn't specific enough or the data slice sent to Gemini was too small.
**Fix:** Tell Antigravity: "The Pattern 1 answer for Question 2 sounds vague. Re-run with more quotes and ask Gemini to be specific about what users say literally."

### Error 2: Quotes don't match the patterns claimed
**Why:** Gemini sometimes picks quotes that don't perfectly fit the pattern it identified.
**Fix:** Add a verification step: after Gemini writes the answer, a second Gemini call checks "do these quotes actually support this pattern?" Antigravity adds this.

### Error 3: Gemini Pro hits a token limit
**Why:** Sending 20 long quotes plus a long prompt can exceed input limits per call.
**Fix:** Truncate quotes to 200 chars before insertion. Antigravity already does this in edge cases, but you may need to lower it further.

---

## How much of my Antigravity credit this uses

Light. The script is straightforward. Estimated agent requests: 8-12.

This phase uses Gemini Pro API requests directly: 7 calls (6 questions + 1 synthesis). Each is a large prompt but well within free tier daily allowance.

---

## What makes this phase special

This is where the project stops being "data engineering" and becomes "product insight." Everything before this phase is plumbing. Everything after this phase is presentation.

The output of Phase 4 is the single most important artifact your PM submission delivers. The Streamlit app in Phase 6 is the wrapping; this report is the gift inside.

---

*End of Phase 4 document. Approve the report quality before moving to Phase 5 (backend orchestration).*
