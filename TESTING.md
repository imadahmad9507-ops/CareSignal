# CareSignal Testing Status

Last verified: September 11, 2026

| Feature | Status | Evidence |
|---|---|---|
| Flask dashboard loads | Working | Flask test client and browser returned HTTP 200 |
| Multiple patient profiles | Working | Create/select flow verified in browser |
| Empty dashboard onboarding | Working | Dashboard has first-patient CTA when no records exist |
| Last checked-in indicator | Working | Dashboard computes today, 1 day ago, or N days ago |
| Daily check-in form | Working | Browser submission redirected to patient detail |
| Journal notes | Working | Notes are stored and shown in history/report |
| Input validation | Working | Missing, malformed, out-of-range, and duplicate dates handled |
| Deterministic risk rules | Working | `test_scenarios.py` covers stable, missing, urgent, borderline, improving |
| Trend arrows | Working | Latest readings compare safely with previous readings |
| Ahmed seed escalation | Working | Stable -> Concerning -> Urgent |
| Chart.js timeline | Working | Canvas renders in browser with oxygen, temperature, and pain |
| Printable report | Working | `/patients/<id>/report` and browser print action verified |
| Safety disclaimer | Working | Visible near top of detail/report/about pages |
| About/safety page | Working | `/about` explains rules versus AI |
| Optional AI success | Working | Mocked success path returns optional AI source |
| AI unavailable/failure fallback | Working | No-key and simulated failure return template text |
| Friendly errors | Working | Custom 404/500 templates and duplicate-date message |

## Known limitations

- The app uses local SQLite and has no authentication; it is a demo prototype, not a production patient-record system.
- Trend arrows describe numeric direction, not whether that direction is medically good or bad.
- Chart.js is loaded from a CDN, so a fully offline browser will not show the chart library.
- The report uses browser print-to-PDF rather than a server-side PDF engine.