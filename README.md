# CareSignal

CareSignal is an explainable, rules-based health trend monitoring prototype for family caregivers. It is a hackathon project using synthetic data, not a medical device or diagnostic system.

## What it does

- Stores patients and daily observations in SQLite.
- Checks oxygen, temperature, breathing difficulty, confusion, pain, and medication adherence.
- Uses deterministic Python rules to assign Stable, Monitor, Concerning, or Urgent status.
- Escalates when a patient's risk is higher than the previous observation.
- Explains the result with a local template by default.
- Optionally uses an OpenAI-compatible API for wording only when `AI_API_KEY` is available. The API cannot change risk or emergency status.
- Visualizes oxygen, temperature, and pain trends with Chart.js.

## Project overview

CareSignal helps family caregivers notice gradual changes in a patient's health across multiple daily check-ins. It is designed for a hackathon demonstration using synthetic data, not for diagnosis, treatment decisions, or emergency response.

The main workflow is simple: create a patient, record an observation, review the current signal, and inspect the trend chart. Each signal includes the readings and rules that caused it, so the result is explainable rather than a mysterious model output.

## Setup on Windows PowerShell

```powershell
cd "C:\Users\Laptop For Sale\Desktop\CareSignal"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
python app.py
```

Open <http://127.0.0.1:5000> in a browser.

## Run the Streamlit version

Install the requirements, seed the demo patient, and start Streamlit:

```powershell
python -m streamlit run streamlit_app.py
```

Streamlit will open the app at <http://localhost:8501>. This is the recommended entry point for Streamlit Community Cloud deployment. In Community Cloud, select `streamlit_app.py` as the main file and add `AI_API_KEY` only if optional AI wording is desired. The app works without secrets.

The app works without an AI key. To enable optional explanation wording through an OpenAI-compatible endpoint, set environment variables before starting Flask:

```powershell
$env:AI_API_KEY = "your-key"
$env:AI_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
$env:AI_MODEL = "gpt-4o-mini"
python app.py
```

Never commit API keys. The default template fallback is the intended no-key demonstration mode.

## How the safety architecture works

1. The check-in is validated and stored locally in SQLite.
2. The pure Python rule engine in `risk_rules.py` checks each reading and compares it with the previous observation.
3. The highest triggered severity becomes the final signal: Stable, Monitor, Concerning, or Urgent.
4. Missing readings are treated as unknown and flagged for monitoring; they are never silently treated as normal.
5. `explanations.py` receives the already-computed signal and reasons. Optional AI can only phrase those facts in plain language.
6. If the AI key is missing, the network fails, or the response is invalid, the local template explanation is returned.

AI cannot determine or override risk or emergency status. The interface repeatedly identifies the prototype as educational and instructs users to contact qualified professionals in an emergency.

## Demo scenario

`python seed.py` creates Ahmed with exactly three observations:

- Day 1: oxygen 96, temperature 37.2, no breathing difficulty -> Stable
- Day 2: oxygen 93, temperature 38.1, mild breathing difficulty -> Concerning
- Day 3: oxygen 89, temperature 38.8, moderate breathing difficulty -> Urgent

Running `python seed.py` again resets Ahmed's observations without creating duplicates.

## Edge-case checks

Run the reproducible rules test from the project directory:

```powershell
python test_scenarios.py
```

It covers stable data, missing readings, a sudden emergency, a borderline reading, and a patient whose condition improves.

The one-page submission copy is in `PROJECT_DESCRIPTION.md` and can be exported or formatted as a PDF for the hackathon submission.

## Project structure

```text
CareSignal/
├── app.py
├── database.py
├── explanations.py
├── risk_rules.py
├── seed.py
├── requirements.txt
├── README.md
├── instance/              # created automatically; SQLite database lives here
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── new_patient.html
│   ├── check_in.html
│   └── patient_detail.html
└── static/
    ├── css/style.css
    └── js/chart.js
```
