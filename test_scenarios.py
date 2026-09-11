from app import app, parse_observation, relative_date, trend_direction
from risk_rules import assess_risk


def show_scenario(label, observation, previous=None, expected=None):
    risk, reasons = assess_risk(observation, previous)
    print(f"\n{label}")
    print(f"  Result: {risk}")
    print(f"  Reasons: {reasons or ['None']}")
    if expected:
        print(f"  Expected: {expected}")
    return risk, reasons


def check(label, condition):
    status = "PASS" if condition else "FAIL"
    print(f"{status}: {label}")
    return condition


if __name__ == "__main__":
    show_scenario(
        "A) Stable patient",
        {
            "oxygen": 98,
            "temperature": 36.8,
            "breathing_difficulty": "none",
            "confusion": "no",
        },
        expected="Stable",
    )

    show_scenario(
        "B) Missing/incomplete data",
        {
            "oxygen": None,
            "temperature": 37.0,
            "breathing_difficulty": "none",
        },
        expected="Handled without a crash; unknown readings should be flagged for monitoring",
    )

    show_scenario(
        "C) Sudden single-day emergency",
        {
            "oxygen": 85,
            "temperature": 39.8,
            "breathing_difficulty": "severe",
            "confusion": "yes",
        },
        expected="Urgent with multiple reasons",
    )

    show_scenario(
        "D) Borderline case",
        {
            "oxygen": 91,
            "temperature": 37.5,
            "breathing_difficulty": "mild",
        },
        expected="Monitor or Concerning; explain the result",
    )

    show_scenario(
        "E1) Improving patient - day 1",
        {
            "oxygen": 90,
            "temperature": 37.5,
            "breathing_difficulty": "none",
            "confusion": "no",
        },
        expected="Concerning",
    )
    show_scenario(
        "E2) Improving patient - day 2",
        {
            "oxygen": 95,
            "temperature": 37.5,
            "breathing_difficulty": "none",
            "confusion": "no",
        },
        previous={
            "oxygen": 90,
            "temperature": 37.5,
            "breathing_difficulty": "none",
            "confusion": "no",
        },
        expected="Stable, with an improvement reason",
    )

    print("\n--- FirstCommit feature checks ---")
    check(
        "Higher oxygen is identified as a raw upward change",
        trend_direction({"oxygen": 98}, {"oxygen": 95}, "oxygen")["symbol"] == "↑",
    )
    check(
        "Missing previous vital is safely marked steady",
        trend_direction({"oxygen": 98}, None, "oxygen")["class"] == "steady",
    )
    check(
        "Notes survive check-in parsing",
        parse_observation(
            {
                "date": "2026-09-11",
                "oxygen": "98",
                "temperature": "36.8",
                "blood_pressure_sys": "120",
                "blood_pressure_dia": "80",
                "breathing_difficulty": "none",
                "pain_level": "1",
                "confusion": "no",
                "medication_adherence": "yes",
                "notes": "Slept well and ate breakfast.",
            }
        )["notes"]
        == "Slept well and ate breakfast.",
    )
    try:
        parse_observation(
            {
                "date": "2026-09-11",
                "oxygen": "140",
                "temperature": "36.8",
                "blood_pressure_sys": "120",
                "blood_pressure_dia": "80",
                "breathing_difficulty": "none",
                "pain_level": "1",
                "confusion": "no",
                "medication_adherence": "yes",
            }
        )
        invalid_data_handled = False
    except ValueError:
        invalid_data_handled = True
    check("Out-of-range oxygen is rejected", invalid_data_handled)
    check("Relative dates produce human-readable text", relative_date("2026-09-09").endswith("days ago"))

    client = app.test_client()
    detail = client.get("/patients/1")
    report = client.get("/patients/1/report")
    about = client.get("/about")
    check("Patient detail includes journal notes column", b"Notes" in detail.data)
    check("Patient detail includes trend indicators", b"DIRECTION SINCE LAST CHECK-IN" in detail.data)
    check("Printable report route renders", report.status_code == 200 and b"Print / Save PDF" in report.data)
    check("About page explains the safety architecture", about.status_code == 200 and b"Rules decide the risk" in about.data)
