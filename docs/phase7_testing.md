# Phase 7 — Testing: Make sure the whole thing actually works

## Goal

The app is built. Every individual piece passed its own tests in earlier phases. But software has a way of failing in ways no individual piece predicted — usually at the seams where pieces connect. This phase is where I (the PM) sit down with the finished app and run through every realistic user scenario, looking for bugs, weird behaviors, and quality issues that only show up in real use. **At the end of this phase, I should be willing to demo the app to a real person without nervousness.**

Think of it like the final walkthrough of a new house before moving in. The contractor (Antigravity) says everything's done. Now I walk through every room, flush every toilet, flip every switch, open every window. Anything that doesn't work right gets fixed before I move my furniture in.

---

## What you'll see when Phase 7 is done

- A document `docs/test_results.md` exists listing every test I ran and its result
- All "must pass" tests have green checkmarks
- A short list of "known issues" with severity (cosmetic vs. functional) and decisions (fix now vs. accept)
- An accuracy spot-check: 50 reviews from the corpus where I personally verified the tags are reasonable
- The insight report has been read carefully and rated for PM-quality (does it answer the questions usefully?)
- Performance numbers: how long does a refresh take, how big is the database, how much memory does the app use

---

## Files created or modified

| File | What it does |
|------|--------------|
| `docs/test_results.md` | The test report — every test ran with its result |
| `docs/known_issues.md` | Bugs found that we decided to defer to Phase 8 or leave |
| `tests/` | Folder with small test scripts (optional but helpful) |
| Bug fixes across multiple files | Whatever needs fixing |

---

## The 8 test scenarios (run them in order)

### Test 1: Fresh setup, no data
**Setup:** Delete reviews.db, restart app.
**Expected:** Dashboard shows empty state with clear "run Refresh" message. No crashes.
**What I'm verifying:** Empty-state handling.

### Test 2: First-ever refresh
**Setup:** Click Refresh on a fresh database.
**Expected:** Progress shows for ~15-25 minutes. Final summary shows ~5,000-8,000 reviews added across 4 sources. Tagging runs. Synthesis runs. Report appears.
**What I'm verifying:** End-to-end happy path.

### Test 3: Incremental refresh (the most important test)
**Setup:** Click Refresh again, 5 minutes after Test 2.
**Expected:** Most scrapers report "0 new reviews" because Reddit/YouTube haven't changed in 5 minutes. Total runtime is under 2 minutes. No duplicate rows added to database.
**What I'm verifying:** The incremental logic isn't lying — it really skips already-seen reviews.

### Test 4: Social media upload
**Setup:** Upload the test_social.csv from Phase 5.
**Expected:** Validation passes. Preview shows 5 rows. After confirm, 5 rows added to database. Run Refresh, they get tagged. Now visible in Q&A.
**What I'm verifying:** The manual upload path works end to end.

### Test 5: Social media upload with bad data
**Setup:** Upload a CSV with wrong columns, or empty rows, or weird encoding (UTF-16 BOM, for example).
**Expected:** Friendly error message that tells me exactly what's wrong. Database is unchanged.
**What I'm verifying:** Error handling is graceful.

### Test 6: Q&A real questions
**Setup:** Ask the Q&A tab these 5 questions one by one:
1. "What do casual listeners say about Discover Weekly?"
2. "Why do power users complain about recommendations?"
3. "What features do users wish existed?"
4. "Is mood-based discovery working for users?"
5. "What's the most common reason users keep listening to the same songs?"

**Expected:** Each answer is specific, cites real reviews, and feels useful. If any answer is vague, generic, or hallucinated, that's a bug.
**What I'm verifying:** The Q&A doesn't just regurgitate the report — it actually retrieves from data.

### Test 7: Manual tag accuracy check
**Setup:** Pull 50 random tagged reviews from the database. Read each review and its tags. Mark ✅ if I agree, ❌ if I don't.
**Expected:** At least 42/50 (84%) agreement.
**What I'm verifying:** The tagger is genuinely accurate, not just confidently wrong.

### Test 8: Report quality check
**Setup:** Read the full insight report top to bottom.
**Expected:** I can imagine handing this to my manager. Patterns are real. Quotes back them up. Segment differences make sense. Unmet needs are insightful, not generic.
**What I'm verifying:** The PM deliverable is actually PM-quality.

---

## Edge cases to specifically test

- **Click Refresh, then immediately click it again** → second click should be ignored, not double-run
- **Upload the same CSV twice in a row** → second upload should report 0 new rows
- **Ask Q&A a question in a different language** ("Pourquoi mes recommandations sont mauvaises?") → should still work
- **Ask Q&A something it can't answer** ("What's the weather?") → should politely redirect
- **Run app, leave browser open for 1 hour, come back** → state should still be there
- **Run pipeline.py from terminal while app is also running** → should detect lock and refuse
- **Delete the latest report file and reload Insights tab** → should fall back to next-most-recent or empty state
- **Type a single character in Q&A and submit** → should reject or handle gracefully

---

## Validation checklist (the BIG one for Phase 7)

Before approving Phase 7, ALL of these must be true:

### Functional
- [ ] All 8 test scenarios pass without bugs
- [ ] All listed edge cases behave correctly
- [ ] No Python errors visible in terminal during normal use
- [ ] Browser console has no red errors when using the app

### Performance
- [ ] First refresh completes in under 30 minutes
- [ ] Incremental refresh (when no new data) completes in under 3 minutes
- [ ] Dashboard loads in under 5 seconds
- [ ] Q&A responses start streaming within 10 seconds
- [ ] Database file size is reasonable (under 100MB even with 10,000 reviews)

### Quality
- [ ] Tag accuracy spot check: ≥84% agreement on 50 random samples
- [ ] Insight report quality: I'd be okay presenting it to a real PM team
- [ ] Q&A answers feel grounded in actual data, not hallucinated

### UI
- [ ] Every tab loads without visual bugs
- [ ] Charts are readable and labeled
- [ ] Text isn't cut off or overlapping
- [ ] Buttons are clearly clickable
- [ ] PDF export produces a real PDF that opens correctly

---

## What I need to do BEFORE Phase 7 starts

Block out 90 uninterrupted minutes. This phase is hands-on — I'm the QA tester. Have:
- The app open in browser
- A timer to measure performance
- A notepad to write down issues
- The 6 PM questions next to me to evaluate the report against them

---

## If something breaks in Phase 7 — what to do

This is the phase where bugs surface, expected to happen. Categorize each bug:

### Category 1: Blocker (fix before approving Phase 7)
- Anything that crashes the app
- Tagging accuracy below 80%
- Refresh button doesn't work
- Q&A returns hallucinated answers

### Category 2: Functional but ugly (fix in Phase 8)
- Charts could be prettier
- Text alignment is off
- Loading indicators could be clearer
- PDF formatting is plain

### Category 3: Acceptable (document and move on)
- One scraper occasionally times out (Reddit's API is finicky)
- One specific edge case I'll never hit in real use

Antigravity should fix Category 1 immediately. Category 2 goes into `docs/known_issues.md` to address in Phase 8. Category 3 just gets logged for transparency.

---

## How much of my Antigravity credit this uses

Variable. If everything just works, this phase is cheap — mostly me clicking around. If bugs surface, each fix costs some agent requests. Estimated: 10-30 depending on number of issues.

---

## What this phase produces for my PM submission

The `docs/test_results.md` file from this phase IS a valuable PM artifact. It demonstrates that I tested the system rigorously, found and fixed real issues, and documented my methodology. Include it in the assignment submission as evidence of thoroughness.

---

*End of Phase 7 document. Approve when all blockers are fixed, then we move to Phase 8 (polish and deliver).*
