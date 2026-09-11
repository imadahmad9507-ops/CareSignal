# CareSignal

## An explainable health trend companion for family caregivers

CareSignal is a Flask web app that helps family caregivers notice gradual changes in a patient's health across daily check-ins. It turns scattered readings and journal notes into a clear timeline, a visible signal, and a printable summary for a conversation with a qualified professional.

### The problem

Health deterioration often does not arrive as one dramatic event. A caregiver may see a slightly lower oxygen reading one day, a higher temperature the next, and new breathing difficulty after that. Without a simple history, those small changes are easy to miss or hard to explain.

### What the project does

CareSignal supports multiple patient profiles, daily observations, caregiver notes, trend charts, raw-direction vital indicators, and a printable patient report. The dashboard shows each patient's current signal and how long it has been since their last check-in. The patient view makes the reasoning visible instead of hiding it behind a score.

The interface also includes a calm dashboard-only animated gradient, subtle page transitions, vital-sign icons, a favicon, and a visual safety-architecture diagram. These are presentation features only: they never affect the data, rules, risk level, or explanation logic.

The demo includes two contrasting profiles. Ahmed's seeded readings move from Stable to Concerning to Urgent across three days, while Fatima's readings remain stable. Caregivers can compare profiles from the dashboard, add a check-in with a journal note, inspect the history, and print a summary.

### How we built it

The project started as a Flask and SQLite prototype. We separated it into a database layer, a pure Python risk engine, an explanation helper, Flask routes, and HTML/CSS/JavaScript templates. Chart.js renders the health timeline in the browser. A lightweight CSS animation gives the dashboard a calm visual identity without introducing a WebGL runtime dependency. Playwright is used by `screenshot_capture.py` to generate reproducible submission screenshots.

The deployment uses a small Vercel Flask adapter in `api/index.py`. Vercel's filesystem is ephemeral, so the public demo stores SQLite under `/tmp` and seeds the two demonstration patients on a fresh instance. This is suitable for a demo, not for durable patient records.

### Safety-first architecture

The risk level is decided by deterministic Python rules. Oxygen, temperature, breathing difficulty, confusion, and change over time can raise the signal from Stable to Monitor, Concerning, or Urgent. The highest triggered rule wins. Optional AI can turn the already-computed reasons into calm plain language, but it cannot create, change, or override a risk decision. If no API key is available or an AI call fails, CareSignal uses a local template and keeps working.

### Honest framing

This is an educational prototype using synthetic data. It adapts the idea behind clinical Early Warning Scores, which help hospital teams notice deterioration, into a simpler home-caregiver workflow. It does not claim to invent a new medical concept, diagnose a condition, or replace professional medical advice. In an emergency, users should contact a doctor or emergency services immediately.

### Technology

Python, Flask, SQLite, plain HTML/CSS/JavaScript, Chart.js, and an optional OpenAI-compatible API used only for explanation wording.

### Challenges we faced

The first challenge was API access. We did not want the project to stop working because an AI key was unavailable, so the explanation layer falls back to local templates whenever there is no key, a network error, a rate limit, or an invalid response.

The second challenge was choosing between Flask and Streamlit. Both versions existed briefly during development. After comparing them, we kept Flask because its multi-page workflow, browser forms, Chart.js detail page, reports, and visual styling were more complete for this general web app submission. We removed the Streamlit entry point rather than leaving two competing frameworks in the final project.

The third challenge was setting a safe AI boundary. We chose rules-based safety logic over pure AI for risk decisions. The rules decide the level and reasons; optional AI only turns those known reasons into plain language. This made the behavior testable and explainable.

Finally, deploying SQLite to Vercel required an honest limitation. Serverless storage is ephemeral, so the deployment automatically seeds demo data but is not presented as a durable medical-record service. Local SQLite remains useful for development and testing.

### What we learned

We learned that a focused rules engine can be more trustworthy than a more ambitious AI feature when the application handles health-related information. We also learned to test the browser experience, not only Python functions: route status, form submission, chart payloads, disclaimers, reports, and screenshot capture all exposed different classes of issues.

Separating the risk engine from the explanation layer made it possible to test missing readings, worsening trends, improving trends, and AI failures independently. Dynamic seed dates also showed the value of treating demo data as part of the product experience: a judge should see current-looking timelines even when opening the project weeks after it was built.

### AI assistance disclosure

AI assistance was used during development to brainstorm scope, review edge cases, generate implementation drafts, and refine documentation. The final application keeps its core risk logic explicit and inspectable, and the optional runtime AI is constrained to explanation text.