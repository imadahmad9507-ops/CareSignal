from risk_rules import assess_risk


def show_scenario(label, observation, previous=None, expected=None):
    risk, reasons = assess_risk(observation, previous)
    print(f"\n{label}")
    print(f"  Result: {risk}")
    print(f"  Reasons: {reasons or ['None']}")
    if expected:
        print(f"  Expected: {expected}")
    return risk, reasons


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
