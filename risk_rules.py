RISK_ORDER = {
    "Stable": 0,
    "Monitor": 1,
    "Concerning": 2,
    "Urgent": 3,
}

def _raise_risk(current_risk, candidate_risk):
    if RISK_ORDER[candidate_risk] > RISK_ORDER[current_risk]:
        return candidate_risk
    return current_risk


def _get_value(observation, field):
    if hasattr(observation, "get"):
        return observation.get(field)
    try:
        return observation[field]
    except (KeyError, IndexError):
        return None


def assess_risk(observation, previous_observation=None):
    """Assess one observation using deterministic, inspectable rules only."""
    risk_level = "Stable"
    reasons = []

    oxygen_value = _get_value(observation, "oxygen")
    temperature_value = _get_value(observation, "temperature")
    oxygen = float(oxygen_value) if oxygen_value is not None else None
    temperature = (
        float(temperature_value) if temperature_value is not None else None
    )
    breathing = _get_value(observation, "breathing_difficulty")
    confusion = _get_value(observation, "confusion")

    missing_fields = [
        field
        for field in ("oxygen", "temperature", "breathing_difficulty", "confusion")
        if _get_value(observation, field) in (None, "")
    ]
    if missing_fields:
        risk_level = _raise_risk(risk_level, "Monitor")
        reasons.append(
            "Some readings are unavailable ("
            + ", ".join(missing_fields)
            + "); no conclusion was made about those readings."
        )

    # Below 90% is a common emergency warning boundary for pulse oximetry.
    if oxygen is not None and oxygen < 90:
        risk_level = _raise_risk(risk_level, "Urgent")
        reasons.append("Oxygen saturation is below the safety threshold.")
    # 90-93% represents a lower-than-normal reading worth prompt attention.
    elif oxygen is not None and 90 <= oxygen <= 93:
        risk_level = _raise_risk(risk_level, "Concerning")
        reasons.append("Oxygen saturation is lower than normal.")

    # 39.5 C marks a high fever in this educational prototype; 38.5 C is
    # retained as a lower concerning boundary so the escalation is gradual.
    if temperature is not None and temperature >= 39.5:
        risk_level = _raise_risk(risk_level, "Urgent")
        reasons.append("High fever detected.")
    elif temperature is not None and temperature >= 38.5:
        risk_level = _raise_risk(risk_level, "Concerning")
        reasons.append("The patient has a fever.")

    # Moderate difficulty warrants concern; severe difficulty is an urgent
    # red flag independent of other readings.
    if breathing == "moderate":
        risk_level = _raise_risk(risk_level, "Concerning")
        reasons.append("Moderate breathing difficulty was reported.")
    elif breathing == "severe":
        risk_level = _raise_risk(risk_level, "Urgent")
        reasons.append(
            "Severe breathing difficulty reported — this requires immediate attention."
        )

    # Combining confusion with oxygen below 94% catches a high-risk pattern
    # that either field alone may not fully describe.
    if confusion == "yes" and oxygen is not None and oxygen < 94:
        risk_level = _raise_risk(risk_level, "Urgent")
        reasons.append(
            "New confusion combined with low oxygen can indicate a serious problem."
        )

    if previous_observation is not None:
        previous_risk, _ = assess_risk(previous_observation)
        if RISK_ORDER[risk_level] > RISK_ORDER[previous_risk]:
            reasons.append("Condition has worsened since the last check-in.")
        elif RISK_ORDER[risk_level] < RISK_ORDER[previous_risk]:
            reasons.append("Condition has improved since the last check-in.")

    return risk_level, reasons
