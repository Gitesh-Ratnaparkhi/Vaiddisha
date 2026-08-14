# src/repositories/database.py
import os
import sqlite3

# Dynamically resolve DB path to project root folder
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "vaiddisha.db"
)


def get_connection():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  conn = get_connection()
  cursor = conn.cursor()

  # 1. Patients Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            email TEXT PRIMARY KEY,
            password TEXT,
            name TEXT,
            gender TEXT,
            age INTEGER,
            country TEXT,
            state TEXT,
            city TEXT,
            postal TEXT,
            phone TEXT,
            preferred_language TEXT,
            existing_conditions TEXT,
            previous_surgeries TEXT,
            allergies TEXT,
            terms_accepted INTEGER DEFAULT 0
        )
    """)

  # 2. Doctors Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            email TEXT PRIMARY KEY,
            password TEXT,
            name TEXT,
            speciality TEXT,
            qualification TEXT,
            experience TEXT,
            hospital TEXT,
            country TEXT,
            state TEXT,
            city TEXT,
            postal TEXT,
            phone TEXT,
            fee TEXT,
            description TEXT,
            terms_accepted INTEGER DEFAULT 0
        )
    """)

  # 3. Consultations History Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_email TEXT,
            patient_name TEXT,
            symptoms TEXT,
            summary TEXT,
            urgency_level TEXT,
            recommended_specialty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

  # 4. Appointments Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_email TEXT,
            patient_name TEXT,
            doctor_email TEXT,
            doctor_name TEXT,
            appointment_date TEXT,
            time_slot TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

  conn.commit()
  conn.close()


# Auto-initialize database on module import
init_db()