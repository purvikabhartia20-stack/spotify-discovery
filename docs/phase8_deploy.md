# Phase 8 — Polish, deploy, and deliver

## Goal

The app works. It's been tested. The data is real, the report is good, the UI is functional. This final phase makes the project submission-ready. We fix the visual polish issues from Phase 7's known_issues list, deploy the app to a public URL so reviewers can actually see it work, export the insight report as a clean PDF, write the methodology section for the PM deliverable, and record a short walkthrough video. **At the end of this phase, I have everything I need to hand in the assignment with confidence.**

Think of it like the last week before a product launch. The product works. Now you're rehearsing the demo, fixing the rough edges, writing the press release, and making sure the launch goes smoothly.

---

## What you'll see when Phase 8 is done

- The app is deployed to **Streamlit Community Cloud** at a public URL (free)
- Anyone with the link can open the app and click around (it uses my data baked in)
- The insight report exists as a polished PDF in `reports/insight_report_FINAL.pdf`
- A `submission/` folder exists containing everything I need to submit
- A 2-minute Loom video shows me walking through the app
- The GitHub repo is cleaned up (README is excellent, no API keys committed)

---

## Files created or modified

| File | What it does |
|------|--------------|
| `README.md` | Updated to be a polished public-facing readme |
| `reports/insight_report_FINAL.pdf` | The submission-ready PDF |
| `submission/` | New folder containing the assignment deliverables |
| `submission/methodology.md` | A short PM-style writeup of the approach |
| `submission/architecture_diagram.png` | A clean diagram of how the system works |
| `submission/sample_quotes.md` | Best 30 user quotes organized by theme |
| `.streamlit/config.toml` | Streamlit cloud deployment config |
| `requirements.txt` | Final, frozen versions for reproducibility |
| `.env.example` | Template for API keys (without real values) |

---

## The 6 sub-tasks of Phase 8

### Sub-task 1: Visual polish
Address everything in `docs/known_issues.md` Category 2:
- Fix chart styling
- Improve loading indicators
- Better empty states
- Mobile responsiveness check
- Color consistency (Spotify green: #1DB954)
- Typography rhythm

### Sub-task 2: Deploy to Streamlit Cloud
1. Push the code to a free GitHub repo
2. Connect Streamlit Community Cloud (free) to the repo
3. Add API keys as Streamlit secrets (not in code)
4. Deploy
5. Get the public URL
6. Test the deployed version end-to-end

### Sub-task 3: Generate the FINAL PDF report
1. Run a fresh refresh to get most current data
2. Generate the report
3. Hand-edit the Markdown for any minor improvements (typos, formatting)
4. Export to a beautifully styled PDF with cover page, table of contents, page numbers
5. Save as `reports/insight_report_FINAL.pdf`

### Sub-task 4: Write the methodology document
A 1-2 page document explaining:
- The problem I was solving
- Why I chose this approach (AI-powered review analysis vs. surveys vs. focus groups)
- The data sources I used and why
- The 6-tag taxonomy I designed
- Limitations of the analysis (sample bias, English-dominant, etc.)
- What I'd do next with more time

This goes in `submission/methodology.md` and becomes part of the PM deliverable.

### Sub-task 5: Architecture diagram
A clean, simple visual showing:
- Data sources (4 boxes on the left)
- Pipeline (middle: scrape → tag → synthesize)
- Output (right: dashboard, report, Q&A)
- Tech stack labels on each component

Export as PNG and put it in submission/.

### Sub-task 6: Loom walkthrough video
A 2-minute screen recording:
- 0:00-0:20 — "I'm building this for a Spotify Growth PM problem about music discovery"
- 0:20-0:50 — Show the Dashboard, explain the data
- 0:50-1:20 — Click Refresh, show how easy it is to update
- 1:20-1:50 — Show the Insights report, highlight one specific finding
- 1:50-2:00 — Ask a question in Q&A, show the answer

This goes into the submission folder as a link.

---

## Edge cases to handle

### Streamlit Cloud deployment
- **Cloud build fails** — usually due to missing system dependencies (weasyprint needs fonts). Add `packages.txt` with required system packages.
- **App is too slow on free Cloud tier** — if cold-start is bad, document it. Worst case, deploy without the live Refresh button (just bake in static data).
- **Secrets management** — never commit config.yaml with real keys. Use Streamlit secrets via `.streamlit/secrets.toml` (gitignored).
- **First time visitor hits an error** — make sure the app gracefully shows demo data if the database is missing.

### PDF export
- **Special characters in user quotes break the PDF** — strip or encode safely
- **PDF is too large** (>20MB) — compress images, reduce font embedding
- **Page breaks are awkward** — add CSS page-break hints in the Markdown-to-HTML step

### GitHub repo
- **API keys accidentally committed** — use `git filter-repo` to remove from history, regenerate compromised keys
- **Repo size too large** (database file committed) — gitignore `*.db` and `data/`
- **README looks raw** — add badges, screenshots, a clear "What is this?" section

### Loom video
- **Audio quality is bad** — use a headset mic, not laptop mic
- **Recording is too long** — practice once, then record. Aim for ≤2 minutes.
- **App is laggy during recording** — pre-cache data, avoid Refresh during recording

---

## Validation checklist (the final one)

- [ ] App is live at a public Streamlit URL — I open it in incognito mode and it works
- [ ] The FINAL PDF opens correctly in Acrobat Reader on a different device
- [ ] README on GitHub looks professional and includes setup, usage, screenshots
- [ ] No API keys, passwords, or secrets are in the git history (run `git log -p | grep -i "api\|secret\|key"`)
- [ ] `submission/` folder is complete: methodology, PDF report, sample quotes, architecture diagram, video link
- [ ] Loom video is recorded, public, and the link works
- [ ] I can hand this entire package to my PM mentor and feel proud of it

---

## What I need to do BEFORE Phase 8 starts

A few small things:
1. Create a free GitHub account if I don't have one
2. Sign up for Streamlit Community Cloud (uses GitHub OAuth, free)
3. Sign up for Loom (free tier allows 25 videos, 5 min each)
4. Have 30 minutes to record the video (maybe 2-3 takes)

---

## If something breaks in Phase 8 — top 3 likely errors

### Error 1: Streamlit Cloud deployment fails with "Module not found"
**Why:** Some libraries (especially scraping ones) need special handling on cloud platforms.
**Fix:** Pin versions in requirements.txt. Add a `packages.txt` with system deps like `wkhtmltopdf` if using pdfkit.

### Error 2: PDF doesn't render emojis from user reviews
**Why:** Default fonts don't support emoji glyphs.
**Fix:** Use a font that does (Noto Color Emoji), or strip emojis from PDF only (keep in app).

### Error 3: Deployed app times out during Refresh
**Why:** Streamlit Cloud free tier has CPU/memory limits and a 30-minute timeout per session.
**Fix:** For the deployed demo, disable the live Refresh button and ship with pre-built data. Mention this in the demo: "On Cloud, data is static. Locally, you can refresh."

---

## How much of my Antigravity credit this uses

Light. Most of Phase 8 is configuration, deployment commands, and content writing. Estimated: 8-15 agent requests.

---

## The final submission package

When Phase 8 is complete, I have:

1. **A live URL** (Streamlit Cloud) — for the assignment reviewer to click
2. **A polished PDF report** — the core insight deliverable
3. **A methodology document** — how I approached the problem
4. **An architecture diagram** — for visual reference
5. **A 2-minute Loom video** — proof of working product
6. **A clean GitHub repo** — for technical credibility
7. **The 8 phase docs from /docs** — methodology transparency

This package shows the reviewer:
- I can identify product problems
- I can architect AI-powered solutions
- I can execute on a non-trivial project
- I can think through edge cases and quality
- I can communicate findings to a PM audience

That's exactly what a Spotify Growth PM hiring committee would want to see.

---

*End of Phase 8 document. End of project. You ship.*
