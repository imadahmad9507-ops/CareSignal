from datetime import date, datetime
import sqlite3

from flask import Flask, flash, redirect, render_template, request, url_for

from database import (
    add_observation,
    add_patient,
    get_connection,
    get_observations,
    get_patient,
    get_patients,
    init_db,
)
from explanations import generate_explanation
from risk_rules import assess_risk


app = Flask(__name__)
app.config["SECRET_KEY"] = "caresignal-development-key"
init_db()


def ensure_demo_data():
    """Repair incomplete public demo data on an ephemeral deployment."""
    if not __import__("os").getenv("VERCEL"):
        return

    from seed import DEMO_OBSERVATIONS, FATIMA_OBSERVATIONS, seed

    patients = get_patients()
    expected = {"Ahmed": len(DEMO_OBSERVATIONS), "Fatima": len(FATIMA_OBSERVATIONS)}
    complete = all(
        any(
            patient["name"] == name
            and len(get_observations(patient["id"])) == observation_count
            for patient in patients
        )
        for name, observation_count in expected.items()
    )
    if not complete:
        seed()


ensure_demo_data()


DISCLAIMER = (
    "This is an educational prototype using synthetic data. It does not diagnose "
    "medical conditions and does not replace professional medical advice. In an "
    "emergency, contact a doctor or emergency services immediately."
)

TREND_FIELDS = (
    "oxygen",
    "temperature",
    "blood_pressure_sys",
    "blood_pressure_dia",
    "pain_level",
)


def trend_direction(current, previous, field):
    """Return a small direction signal without assigning clinical meaning."""
    if previous is None or current[field] is None or previous[field] is None:
        return {"symbol": "→", "label": "No previous reading", "class": "steady"}
    if float(current[field]) > float(previous[field]):
        return {"symbol": "↑", "label": "Higher than previous", "class": "up"}
    if float(current[field]) < float(previous[field]):
        return {"symbol": "↓", "label": "Lower than previous", "class": "down"}
    return {"symbol": "→", "label": "Unchanged", "class": "steady"}


def relative_date(value):
    try:
        checked_date = datetime.strptime(str(value), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return "date unavailable"
    days = (date.today() - checked_date).days
    if days < 0:
        return "future date"
    if days == 0:
        return "today"
    if days == 1:
        return "1 day ago"
    return f"{days} days ago"


def observation_assessment(observations):
    assessed = []
    for index, observation in enumerate(observations):
        previous = observations[index - 1] if index else None
        risk, reasons = assess_risk(observation, previous)
        explanation, source = generate_explanation(risk, reasons)
        trends = {
            field: trend_direction(observation, previous, field)
            for field in TREND_FIELDS
        }
        assessed.append(
            {
                "observation": observation,
                "risk": risk,
                "reasons": reasons,
                "explanation": explanation,
                "source": source,
                "trends": trends,
            }
        )
    return assessed


def parse_observation(form):
    breathing = form.get("breathing_difficulty", "none")
    confusion = form.get("confusion", "no")
    adherence = form.get("medication_adherence", "yes")
    if breathing not in {"none", "mild", "moderate", "severe"}:
        raise ValueError("Choose a valid breathing difficulty level.")
    if confusion not in {"yes", "no"} or adherence not in {"yes", "no"}:
        raise ValueError("Choose valid yes/no values.")

    try:
        values = {
            "date": form.get("date", ""),
            "oxygen": float(form["oxygen"]),
            "temperature": float(form["temperature"]),
            "blood_pressure_sys": int(form["blood_pressure_sys"]),
            "blood_pressure_dia": int(form["blood_pressure_dia"]),
            "breathing_difficulty": breathing,
            "pain_level": int(form["pain_level"]),
            "confusion": confusion,
            "medication_adherence": adherence,
            "notes": form.get("notes", "").strip(),
        }
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Enter a number in every required reading field.") from error

    if not values["date"]:
        raise ValueError("Choose an observation date.")
    try:
        datetime.strptime(values["date"], "%Y-%m-%d")
    except ValueError as error:
        raise ValueError("Use a valid observation date.") from error
    if not 0 <= values["oxygen"] <= 100:
        raise ValueError("Oxygen saturation must be between 0 and 100%.")
    if not 32 <= values["temperature"] <= 43:
        raise ValueError("Temperature must be between 32°C and 43°C.")
    if not 40 <= values["blood_pressure_sys"] <= 300:
        raise ValueError("Systolic blood pressure must be between 40 and 300.")
    if not 20 <= values["blood_pressure_dia"] <= 200:
        raise ValueError("Diastolic blood pressure must be between 20 and 200.")
    if not 0 <= values["pain_level"] <= 10:
        raise ValueError("Pain level must be between 0 and 10.")
    return values


@app.template_filter("date_label")
def date_label(value):
    return value.strftime("%b %d, %Y").replace(" 0", " ") if hasattr(value, "strftime") else value


@app.route("/")
def dashboard():
    patient_cards = []
    for patient in get_patients():
        observations = get_observations(patient["id"])
        assessed = observation_assessment(observations)
        latest = assessed[-1] if assessed else None
        patient_cards.append(
            {
                "patient": patient,
                "latest": latest,
                "last_checked": relative_date(latest["observation"]["date"])
                if latest
                else None,
            }
        )
    return render_template("dashboard.html", patient_cards=patient_cards, body_class="dashboard-page")


@app.route("/patients/new", methods=["GET", "POST"])
def new_patient():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Enter a patient name.", "error")
        else:
            patient_id = add_patient(name)
            return redirect(url_for("check_in", patient_id=patient_id))
    return render_template("new_patient.html")


@app.route("/patients/<int:patient_id>/check-in", methods=["GET", "POST"])
def check_in(patient_id):
    patient = get_patient(patient_id)
    if patient is None:
        return "Patient not found", 404
    if request.method == "POST":
        try:
            add_observation(patient_id, parse_observation(request.form))
            flash("Daily check-in saved.", "success")
            return redirect(url_for("patient_detail", patient_id=patient_id))
        except sqlite3.IntegrityError:
            flash("A check-in already exists for this patient on that date. Choose another date.", "error")
        except (KeyError, ValueError) as error:
            flash(str(error), "error")
    return render_template("check_in.html", patient=patient, today=date.today().isoformat())


@app.route("/patients/<int:patient_id>")
def patient_detail(patient_id):
    patient = get_patient(patient_id)
    if patient is None:
        return "Patient not found", 404
    observations = get_observations(patient_id)
    assessed = observation_assessment(observations)
    latest = assessed[-1] if assessed else None
    chart_data = [dict(item) for item in observations]
    return render_template(
        "patient_detail.html",
        patient=patient,
        assessed=assessed,
        latest=latest,
        chart_data=chart_data,
        disclaimer=DISCLAIMER,
    )


@app.route("/patients/<int:patient_id>/report")
def patient_report(patient_id):
    patient = get_patient(patient_id)
    if patient is None:
        return "Patient not found", 404
    assessed = observation_assessment(get_observations(patient_id))
    return render_template(
        "report.html",
        patient=patient,
        assessed=assessed,
        latest=assessed[-1] if assessed else None,
        disclaimer=DISCLAIMER,
        generated_on=date.today(),
    )


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404, message="That page could not be found."), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", code=500, message="Something went wrong. Please try again."), 500


@app.cli.command("reset-db")
def reset_db():
    with get_connection() as connection:
        connection.executescript(
            "DROP TABLE IF EXISTS observations; DROP TABLE IF EXISTS patients;"
        )
    init_db()
    print("Database reset.")


if __name__ == "__main__":
    app.run(debug=True)
