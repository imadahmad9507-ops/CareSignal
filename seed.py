from database import add_observation, add_patient, get_connection, get_patients, init_db


DEMO_OBSERVATIONS = [
    {
        "date": "2026-09-07",
        "oxygen": 96,
        "temperature": 37.2,
        "blood_pressure_sys": 120,
        "blood_pressure_dia": 80,
        "breathing_difficulty": "none",
        "pain_level": 1,
        "confusion": "no",
        "medication_adherence": "yes",
        "notes": "Feeling normal.",
    },
    {
        "date": "2026-09-08",
        "oxygen": 93,
        "temperature": 38.1,
        "blood_pressure_sys": 124,
        "blood_pressure_dia": 82,
        "breathing_difficulty": "mild",
        "pain_level": 3,
        "confusion": "no",
        "medication_adherence": "yes",
        "notes": "More tired than usual.",
    },
    {
        "date": "2026-09-09",
        "oxygen": 89,
        "temperature": 38.8,
        "blood_pressure_sys": 128,
        "blood_pressure_dia": 84,
        "breathing_difficulty": "moderate",
        "pain_level": 6,
        "confusion": "no",
        "medication_adherence": "yes",
        "notes": "Breathing is more difficult today.",
    },
]


def seed():
    init_db()
    existing = next((patient for patient in get_patients() if patient["name"] == "Ahmed"), None)
    if existing:
        patient_id = existing["id"]
        with get_connection() as connection:
            connection.execute("DELETE FROM observations WHERE patient_id = ?", (patient_id,))
    else:
        patient_id = add_patient("Ahmed")

    for observation in DEMO_OBSERVATIONS:
        add_observation(patient_id, observation)
    print(f"Seeded Ahmed with {len(DEMO_OBSERVATIONS)} observations.")


if __name__ == "__main__":
    seed()
