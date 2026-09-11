from datetime import date
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


DISCLAIMER = (
    "This is an educational prototype using synthetic data. It does not diagnose "
    "medical conditions and does not replace professional medical advice. In an "
    "emergency, contact a doctor or emergency services immediately."
)


def observation_assessment(observations):
    assessed = []
    for index, observation in enumerate(observations):
        previous = observations[index - 1] if index else None
        risk, reasons = assess_risk(observation, previous)
        explanation, source = generate_explanation(risk, reasons)
        assessed.append(
            {
                "observation": observation,
                "risk": risk,
                "reasons": reasons,
                "explanation": explanation,
                "source": source,
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
    if not values["date"]:
        raise ValueError("Choose an observation date.")
    if not 0 <= values["pain_level"] <= 10:
        raise ValueError("Pain level must be between 0 and 10.")
    if not 50 <= values["oxygen"] <= 100:
        raise ValueError("Oxygen saturation must be between 50 and 100.")
    return values


@app.template_filter("date_label")
def date_label(value):
    return value.strftime("%b %-d, %Y") if hasattr(value, "strftime") else value


@app.route("/")
def dashboard():
    patient_cards = []
    for patient in get_patients():
        observations = get_observations(patient["id"])
        assessed = observation_assessment(observations)
        latest = assessed[-1] if assessed else None
        patient_cards.append({"patient": patient, "latest": latest})
    return render_template("dashboard.html", patient_cards=patient_cards)


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
