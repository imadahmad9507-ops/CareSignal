# CareSignal

## An explainable early-warning companion for family caregivers

### The problem

Family caregivers often miss gradual health deterioration because changes happen slowly across days, not in a single dramatic moment. A small drop in oxygen, a rising temperature, or new breathing difficulty can be hard to interpret when observations are scattered across memory, notes, and conversations.

### The solution

CareSignal is a health trend monitoring prototype that lets caregivers record daily observations such as oxygen saturation, temperature, blood pressure, breathing difficulty, pain, confusion, and medication adherence. Transparent, deterministic rules analyze each check-in and compare it with the previous reading to identify worsening trends.

The system explains its result in plain language. If an optional AI service is configured, AI may help phrase that explanation for a non-medical caregiver. AI never determines the risk level, never sets emergency status, and cannot override the rule engine. The safety rules always decide.

### Honest framing

CareSignal adapts the idea behind Early Warning Scores, which are used in hospitals to help teams notice patient deterioration, into an accessible experience for home caregivers. It does not claim to invent an entirely new medical concept. Its contribution is making an existing safety practice easier to use outside a hospital, with visible reasoning that caregivers can understand.

### Key features

- A caregiver dashboard with each patient's current signal and last check-in.
- A daily check-in for core readings and observable symptoms.
- A risk trend chart showing oxygen, temperature, and pain across logged days.
- Safety overrides where deterministic rules always control the final status.
- Plain-language explanations and explicit reasons for each signal.
- Clear escalation from Stable to Monitor, Concerning, or Urgent.

### Safety statement

CareSignal is an educational prototype using synthetic data. It is not a diagnostic tool, does not diagnose medical conditions, and does not replace professional medical advice. In an emergency, users should contact a doctor or emergency services immediately.

### Technology

- Python and Flask for the backend
- SQLite for local data storage
- Plain HTML, CSS, and JavaScript for the interface
- Chart.js for the trend visualization
- Optional OpenAI-compatible API for explanation wording only

CareSignal is designed to make changes visible, reasoning inspectable, and the boundary between software assistance and professional medical care clear.
