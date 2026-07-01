# Phase 6 — Frontend: The Streamlit web app

## Goal

This is where the project transforms from "a Python script I run in a terminal" into "a real web app I can click around in." We build a five-tab interface that lets me see charts, click a Refresh button to pull new data, upload social media CSVs, read the insight report, and chat with my own data. **At the end of this phase, opening the app on my laptop feels like using a polished SaaS product, not a research project.**

Think of it like the dashboard of a car. The engine (Phase 5) is already built and running. Now we add the steering wheel, speedometer, gas gauge, radio, and AC controls so the driver can actually interact with the car. The engine doesn't change — we're just making it usable.

---

## What you'll see when Phase 6 is done

- A file `app.py` exists at the project root
- Running `streamlit run app.py` opens my web browser to `http://localhost:8501`
- The browser shows a clean app with the title "Spotify Discovery Engine"
- Five tabs across the top: Dashboard, Refresh Data, Insights Report, Ask Q&A, Upload Social Data
- The Dashboard shows real charts with real data — not placeholder data
- Clicking "Refresh All Data" actually triggers pipeline.py and shows live progress
- The CSV upload tab accepts a file and confirms it was processed
- The Insights tab renders the latest insight report in clean Markdown
- The Q&A tab lets me type a question, sends it to Gemini with my review data as context, and shows the answer with citations
- An "Export Report as PDF" button on the Insights tab actually produces a downloadable PDF

---

## Files created or modified

| File | What it does |
|------|--------------|
| `app.py` | The Streamlit web app, all 5 tabs in one file |
| `ui/` | Folder for helper UI modules (charts, styling) |
| `ui/charts.py` | Plotly chart functions: theme bar chart |
| `ui/styles.py` | Custom CSS to make the app look polished (Spotify green accent) |
| `ui/qa.py` | The Q&A logic — sends user question + review context to Gemini Pro |
| `agents/export_pdf.py` | Converts the Markdown report to PDF |
| `requirements.txt` | Updated with streamlit, plotly, pdfkit/weasyprint |

---

## The 5 tabs — what each one shows

### Tab 1: Dashboard (the landing page)
At the top: 4 metric cards
- Total reviews in corpus
- Reviews added since last refresh
- Date of last refresh


Below: 4 charts in a 2×2 grid
- Theme breakdown (bar chart, biggest to smallest, "Other" excluded to avoid clutter)

- Top pain points table (sortable, with severity score)

Below that: A small list "Recent high-severity reviews" with 5 examples

### Tab 2: Refresh
A big "Refresh All Data" button at the top. Below it, status text.

When I click the button:
- The button greys out and shows "Running..."
- A live status box appears showing each step: "Scraping Play Store [50/2000]", "Scraping Reddit [post 23 of 50]" etc.
- A progress bar fills as steps complete
- When done, shows a green "✅ Refresh complete" with stats

Below the button: "Recent runs" table showing last 10 refreshes with date, duration, new reviews, errors.

### Tab 5: Upload Social Data
A file uploader widget for CSV files. Instructions next to it explaining the expected format with a downloadable template/sample CSV.

When I upload a file:
- The app parses it for `platform` and `content`
- Shows me a preview of the first few rows
- A "Process & Insert to Database" button appears
- After clicking, it hashes and injects the raw text into the SQLite DB so it can be tagged on the next Refresh.

### Tab 4: Insights
The Markdown insight report rendered cleanly on the page. Section headers act as a left-sidebar nav: jump to Question 1, 2, 3 etc.

Top of tab: dropdown to switch between reports (today's, yesterday's, last week's).
Top right: "Export as PDF" button that produces a downloadable PDF.

If no report exists yet: a friendly "Run a refresh first to generate insights" message with link to Refresh tab.

### Tab 5: Q&A
A chat-style interface at the bottom of the screen with a text input.

When I type a question (e.g. "What do power users say about Discover Weekly?"):
- The app pulls relevant tagged reviews from the database (top 30 by relevance using simple keyword + theme match)
- Sends them to Gemini 2.5 Pro along with my question as context
- Streams the answer back to me
- At the bottom of the answer: "Based on 30 reviews from your corpus" with expandable list of which reviews were used as evidence

Chat history persists for the current session so I can ask follow-up questions.

### Deep Dive: Review Explorer
A dedicated section in the Dashboard Tab that lets you read the raw data:
- Filter by Source (App Store, Play Store, Reddit, YouTube, Twitter, Instagram)
- Filter by Theme
- See exactly what real users wrote.

---

## Step-by-step plan

1. **Set up the app skeleton** — Streamlit page config (title, icon, layout=wide), the 5 tabs using `st.tabs()`
2. **Build the styles module** — CSS to add Spotify-green accents, clean typography, proper spacing
3. **Build the chart functions** — each chart takes data from the database and returns a Plotly figure
4. **Build the Dashboard tab** — load data, render metrics, render charts
5. **Build the Refresh tab** — button that calls pipeline.py as a subprocess, captures stdout, streams it to the UI
6. **Build the Social Upload tab** — file uploader, validator, preview, confirm flow
7. **Build the Insights tab** — file picker for which report to view, render Markdown, PDF export button
8. **Build the Q&A tab** — text input, retrieval logic, Gemini Pro call with streaming
9. **Add cache decorators** so the dashboard doesn't reload data on every tab switch
10. **Add a sidebar** with project info, link to GitHub (if used), version number
11. **Test all 5 tabs work** and look polished

---

## Edge cases to handle

### Refresh tab
- **User clicks Refresh while one is already running** → button disabled, show "Run in progress"
- **Pipeline takes > 30 minutes** → Streamlit may time out, so we use `st.spinner` and async updates
- **Pipeline fails mid-run** → show clear error message with which step failed
- **User closes browser tab during refresh** → pipeline keeps running in background; reopening the app shows it's still going

### Social Upload tab
- **User uploads non-CSV file** (Excel, PDF) → friendly rejection with message "Please upload a .csv file. Need help converting?"
- **CSV is >10MB** → warn user it'll take a few minutes, offer to break into chunks
- **CSV has no rows after header** → reject with "This CSV looks empty"
- **CSV upload succeeds but tagging hasn't run yet** → show "Uploaded. Run Refresh to tag and include in insights."

### Insights tab
- **No reports exist** → friendly empty state
- **PDF export fails** (weasyprint can be finicky) → fallback to plain HTML download
- **Report is very long** → use Streamlit's expandable sections per question

### Q&A tab
- **User asks question unrelated to reviews** (e.g. "what's the weather") → Gemini responds based on reviews only and says "I can only answer about your review corpus"
- **No reviews match the question's topic** → show "No relevant reviews found. Try rephrasing."
- **User hits Gemini API quota** → show friendly message "Daily Gemini limit reached. Resets at midnight UTC."

### Universal
- **Database is empty** (first run, nothing scraped) → Dashboard tab shows empty state with arrow pointing to Refresh tab
- **Plotly chart fails to render** (some dataset edge case) → show fallback table
- **Streamlit Cloud deployment has different file paths** → use absolute paths via `pathlib`

---

## Validation checklist (for me to tick off before approving Phase 6)

- [ ] `streamlit run app.py` opens the app in my browser without errors
- [ ] All 5 tabs load without errors
- [ ] The Dashboard shows real data, real numbers, real charts
- [ ] Clicking Refresh runs the actual pipeline and shows progress
- [ ] I can upload my test_social.csv and see it succeed
- [ ] The Insights tab renders my latest report cleanly
- [ ] I can click "Export PDF" and download a real PDF
- [ ] In Q&A, I can ask "What do users complain about most?" and get a real answer with citations
- [ ] The app looks polished — not raw Streamlit default styling
- [ ] If I refresh the browser, all my data is still there

---

## What I need to do BEFORE Phase 6 starts

Nothing technical. Be ready to test each tab as Antigravity finishes building it. Take screenshots of anything that looks wrong — sometimes UI issues are subtle and a screenshot helps Antigravity fix faster than a description.

---

## If something breaks in Phase 6 — top 3 likely errors

### Error 1: "ModuleNotFoundError: No module named 'streamlit'"
**Why:** Streamlit wasn't installed yet because we added it in this phase.
**Fix:** `pip install streamlit plotly weasyprint` — Antigravity does this automatically before running.

### Error 2: Refresh button click doesn't show live progress
**Why:** Streamlit's display updates work differently from terminal output. Naively calling pipeline.py won't stream to the UI.
**Fix:** Wrap pipeline calls in `st.status` containers and pipe stdout through a generator. Antigravity knows this pattern.

### Error 3: PDF export produces broken or empty PDF
**Why:** weasyprint sometimes has issues with system fonts or special characters in Markdown.
**Fix:** Use `pdfkit` as fallback OR convert Markdown → HTML → PDF via an explicit two-step process. Antigravity handles this.

### Error 4 (common): Charts look squished or weird
**Why:** Streamlit's default column widths don't always cooperate with Plotly's responsive sizing.
**Fix:** Add `use_container_width=True` to every Plotly call. One-line fix.

---

## How much of my Antigravity credit this uses

Moderate to heavy — UI work tends to need more iteration than backend. Estimated agent requests: 20-30. If first attempt looks weak visually, expect another 10 requests for polish.

---

## What "polished" looks like vs default Streamlit

Default Streamlit looks like a Jupyter notebook. We want something that looks like a real product:
- Custom CSS for typography
- Spotify-green accent color throughout
- Generous whitespace, no cramped layouts
- Clear visual hierarchy (titles, subtitles, body text)
- Icons next to section headers (using emoji or Tabler icons)
- Mobile-responsive (Streamlit handles this automatically but verify)
- A small sidebar with project name and last refresh time always visible

If after Phase 6 the UI looks too plain, I can ask Antigravity in Phase 8 (polish) to take another pass.

---

*End of Phase 6 document. Approve and we move to Phase 7 (integration testing).*
