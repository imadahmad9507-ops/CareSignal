from datetime import date, timedelta

from database import add_observation, add_patient, get_connection, get_patients, init_db


today = date.today()
ahmed_day1 = today - timedelta(days=4)
ahmed_day2 = today - timedelta(days=3)
ahmed_day3 = today - timedelta(days=2)
fatima_day1 = today - timedelta(days=2)
fatima_day2 = today - timedelta(days=1)
fatima_day3 = today


DEMO_OBSERVATIONS = [
    {
        "date": ahmed_day1.isoformat(),
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
        "date": ahmed_day2.isoformat(),
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
        "date": ahmed_day3.isoformat(),
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

FATIMA_OBSERVATIONS = [
    {
        "date": fatima_day1.isoformat(),
        "oxygen": 98,
        "temperature": 36.7,
        "blood_pressure_sys": 118,
        "blood_pressure_dia": 76,
        "breathing_difficulty": "none",
        "pain_level": 0,
        "confusion": "no",
        "medication_adherence": "yes",
        "notes": "Feeling well and following the normal routine.",
    },
    {
        "date": fatima_day2.isoformat(),
        "oxygen": 97,
        "temperature": 36.8,
        "blood_pressure_sys": 119,
        "blood_pressure_dia": 77,
        "breathing_difficulty": "none",
        "pain_level": 1,
        "confusion": "no",
        "medication_adherence": "yes",
        "notes": "No new concerns reported.",
    },
    {
        "date": fatima_day3.isoformat(),
        "oxygen": 98,
        "temperature": 36.6,
        "blood_pressure_sys": 117,
        "blood_pressure_dia": 75,
        "breathing_difficulty": "none",
        "pain_level": 0,
        "confusion": "no",
        "medication_adherence": "yes",
        "notes": "Stable check-in.",
    },
]


def seed_patient(name, observations):
    existing = next((patient for patient in get_patients() if patient["name"] == name), None)
    if existing:
        patient_id = existing["id"]
        with get_connection() as connection:
            connection.execute("DELETE FROM observations WHERE patient_id = ?", (patient_id,))
    else:
        patient_id = add_patient(name)

    for observation in observations:
        add_observation(patient_id, observation)
    return patient_id


def seed():
    init_db()
    # Demo data is intentionally deterministic so screenshots and judge reviews
    # always start with the same two contrasting patient profiles.
    seed_patient("Ahmed", DEMO_OBSERVATIONS)
    seed_patient("Fatima", FATIMA_OBSERVATIONS)
    print(f"Seeded Ahmed with {len(DEMO_OBSERVATIONS)} observations.")
    print(f"Seeded Fatima with {len(FATIMA_OBSERVATIONS)} observations.")


if __name__ == "__main__":
    seed()
