# src/repositories/database.py
import sqlite3

DB_PATH = "vaiddisha.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Base Users Auth Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash BLOB NOT NULL,
            role TEXT NOT NULL,
            terms_accepted INTEGER DEFAULT 0
        )
    """)

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN terms_accepted INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    # 2. Patients Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT,
            age INTEGER,
            country TEXT,
            state TEXT,
            city TEXT,
            postal_code TEXT,
            phone TEXT,
            preferred_language TEXT,
            existing_conditions TEXT,
            previous_surgeries TEXT,
            allergies TEXT,
            FOREIGN KEY (email) REFERENCES users (email) ON DELETE CASCADE
        )
    """)

    # 3. Doctors Table (Updated with description)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            speciality TEXT NOT NULL,
            qualification TEXT,
            experience TEXT,
            hospital TEXT,
            country TEXT,
            state TEXT,
            city TEXT,
            postal_code TEXT,
            phone TEXT,
            fee TEXT,
            description TEXT,
            FOREIGN KEY (email) REFERENCES users (email) ON DELETE CASCADE
        )
    """)

    # Auto-migration for existing DB
    try:
        cursor.execute("ALTER TABLE doctors ADD COLUMN description TEXT")
    except sqlite3.OperationalError:
        pass

    # 4. Consultations History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_email TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            summary TEXT,
            urgency_level TEXT,
            recommended_specialty TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_email) REFERENCES users (email)
        )
    """)

    conn.commit()
    conn.close()

init_db()