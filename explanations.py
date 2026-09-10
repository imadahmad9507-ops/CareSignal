import json
import os
import urllib.request


CLOSING_LINES = {
    "Urgent": "Please seek urgent medical attention now.",
    "Concerning": "Please contact a healthcare professional soon.",
    "Monitor": "Keep monitoring and note any changes.",
    "Stable": "No concerning changes detected. Continue regular monitoring.",
}


def template_explanation(risk_level, reasons):
    reason_text = " ".join(reasons) if reasons else "No concerning changes were detected."
    return f"Your readings show a {risk_level} status. {reason_text} {CLOSING_LINES[risk_level]}"


def _recommendation(risk_level):
    if risk_level == "Urgent":
        return "seek urgent care"
    if risk_level == "Concerning":
        return "contact a doctor"
    return "continue monitoring"


def _call_openai_compatible(prompt, api_key, endpoint):
    payload = {
        "model": os.getenv("AI_MODEL", "gpt-4o-mini"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 160,
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=8) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def generate_explanation(risk_level, reasons):
    """Use optional AI only for wording; rules remain the source of risk truth."""
    api_key = os.getenv("AI_API_KEY")
    if not api_key:
        return template_explanation(risk_level, reasons), "template"

    prompt = (
        "Explain this health risk assessment to a non-medical caregiver in 2-3 "
        "simple, calm sentences. Do not diagnose and do not add medical claims "
        "beyond the listed reasons. End with the requested recommendation. "
        f"Risk level: {risk_level}. Detected reasons: {reasons}. "
        f"Recommendation: {_recommendation(risk_level)}."
    )
    endpoint = os.getenv(
        "AI_API_ENDPOINT", "https://api.openai.com/v1/chat/completions"
    )
    try:
        explanation = _call_openai_compatible(prompt, api_key, endpoint)
        if explanation:
            return explanation, "optional AI"
    except Exception:
        pass

    return template_explanation(risk_level, reasons), "template fallback"
