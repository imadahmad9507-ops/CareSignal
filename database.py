from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent
# Vercel functions can write only to /tmp; local development keeps instance/.
INSTANCE_DIR = Path("/tmp/caresignal") if Path("/tmp").exists() and __import__("os").getenv("VERCEL") else BASE_DIR / "instance"
DATABASE_PATH = INSTANCE_DIR / "caresignal.db"


def get_connection():
    INSTANCE_DIR.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                oxygen REAL NOT NULL,
                temperature REAL NOT NULL,
                blood_pressure_sys INTEGER NOT NULL,
                blood_pressure_dia INTEGER NOT NULL,
                breathing_difficulty TEXT NOT NULL CHECK (
                    breathing_difficulty IN ('none', 'mild', 'moderate', 'severe')
                ),
                pain_level INTEGER NOT NULL CHECK (pain_level BETWEEN 0 AND 10),
                confusion TEXT NOT NULL CHECK (confusion IN ('yes', 'no')),
                medication_adherence TEXT NOT NULL CHECK (
                    medication_adherence IN ('yes', 'no')
                ),
                notes TEXT NOT NULL DEFAULT '',
                UNIQUE(patient_id, date),
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_observations_patient_date
            ON observations(patient_id, date);
            """
        )


def get_patient(patient_id):
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM patients WHERE id = ?", (patient_id,)
        ).fetchone()


def get_patients():
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM patients ORDER BY name COLLATE NOCASE"
        ).fetchall()


def get_observations(patient_id):
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT * FROM observations
            WHERE patient_id = ?
            ORDER BY date ASC, id ASC
            """,
            (patient_id,),
        ).fetchall()


def add_patient(name):
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO patients (name) VALUES (?)", (name.strip(),)
        )
        return cursor.lastrowid


def add_observation(patient_id, values):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO observations (
                patient_id, date, oxygen, temperature, blood_pressure_sys,
                blood_pressure_dia, breathing_difficulty, pain_level, confusion,
                medication_adherence, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                values["date"],
                values["oxygen"],
                values["temperature"],
                values["blood_pressure_sys"],
                values["blood_pressure_dia"],
                values["breathing_difficulty"],
                values["pain_level"],
                values["confusion"],
                values["medication_adherence"],
                values["notes"],
            ),
        )
        return cursor.lastrowid
