# Phase 7 Known Issues

Use this document to log any bugs or oddities found during the Phase 7 Testing Walkthrough. 

Blocker bugs (Category 1) should be fixed immediately and not left in this document. Only log Category 2 and Category 3 bugs here.

*(Note: We encountered a Category 1 Blocker bug where asking a Q&A question with an apostrophe (like "What's") crashed the app due to a SQL injection/syntax error. This was fixed immediately in Phase 7).*

---

## Category 2: Functional but ugly
*Bugs to be fixed in Phase 8 (Polish & Deliver).*

1. **Issue:** Q&A Tab throws ugly rate-limit traces (429 errors) when typing multiple questions quickly.
   - **Impact:** Scares the user and looks broken, even though it's just a free-tier API limit.
   - **Resolution Plan:** Catch 429 Resource Exhausted errors in `app.py` and display a friendly "Gemini API is busy, please wait 5 seconds" message instead of a raw stack trace.

## Category 3: Acceptable
*Bugs or quirks that we are intentionally deciding NOT to fix.*

1. **Issue:** "First-ever refresh" takes 45+ minutes on a fresh database.
   - **Why Acceptable:** This is entirely bottlenecked by the Google Gemini API Free Tier rate limit (15 requests per minute). Since this app is a prototype and not paying for an enterprise API key, tagging 500+ reviews sequentially will always be slow. Incremental runs are fast.
