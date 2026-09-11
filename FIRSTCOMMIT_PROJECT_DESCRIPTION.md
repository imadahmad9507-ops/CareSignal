# CareSignal

## An explainable health trend companion for family caregivers

CareSignal is a Flask web app that helps family caregivers notice gradual changes in a patient's health across daily check-ins. It turns scattered readings and journal notes into a clear timeline, a visible signal, and a printable summary for a conversation with a qualified professional.

### The problem

Health deterioration often does not arrive as one dramatic event. A caregiver may see a slightly lower oxygen reading one day, a higher temperature the next, and new breathing difficulty after that. Without a simple history, those small changes are easy to miss or hard to explain.

### What I built

CareSignal supports multiple patient profiles, daily observations, caregiver notes, trend charts, raw-direction vital indicators, and a printable patient report. The dashboard shows each patient's current signal and how long it has been since their last check-in. The patient view makes the reasoning visible instead of hiding it behind a score.

The interface also includes a calm dashboard-only animated gradient, subtle page transitions, vital-sign icons, a favicon, and a visual safety-architecture diagram. These are presentation features only: they never affect the data, rules, risk level, or explanation logic.

### Safety-first architecture

The risk level is decided by deterministic Python rules. Oxygen, temperature, breathing difficulty, confusion, and change over time can raise the signal from Stable to Monitor, Concerning, or Urgent. The highest triggered rule wins. Optional AI can turn the already-computed reasons into calm plain language, but it cannot create, change, or override a risk decision. If no API key is available or an AI call fails, CareSignal uses a local template and keeps working.

### Honest framing

This is an educational prototype using synthetic data. It adapts the idea behind clinical Early Warning Scores, which help hospital teams notice deterioration, into a simpler home-caregiver workflow. It does not claim to invent a new medical concept, diagnose a condition, or replace professional medical advice. In an emergency, users should contact a doctor or emergency services immediately.

### Technology

Python, Flask, SQLite, plain HTML/CSS/JavaScript, Chart.js, and an optional OpenAI-compatible API used only for explanation wording.

### AI assistance disclosure

AI assistance was used during development to brainstorm scope, review edge cases, generate implementation drafts, and refine documentation. The final application keeps its core risk logic explicit and inspectable, and the optional runtime AI is constrained to explanation text.