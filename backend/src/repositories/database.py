# backend/src/repositories/database.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing in your backend/.env file!")

def get_db_connection():
    """Establishes a connection to the PostgreSQL database returning dict-like rows."""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

# Alias for compatibility
get_connection = get_db_connection

def init_db():
    """Initializes all PostgreSQL tables if they don't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        email VARCHAR(255) PRIMARY KEY,
        password_hash TEXT NOT NULL,
        role VARCHAR(50) NOT NULL CHECK(role IN ('Patient', 'Doctor')),
        terms_accepted BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Patients Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        email VARCHAR(255) PRIMARY KEY REFERENCES users(email) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        gender VARCHAR(50),
        age INTEGER,
        country VARCHAR(100),
        state VARCHAR(100),
        city VARCHAR(100),
        postal_code VARCHAR(50),
        phone VARCHAR(50),
        language VARCHAR(50) DEFAULT 'English',
        conditions TEXT,
        surgeries TEXT,
        allergies TEXT
    );
    """)

    # 3. Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        email VARCHAR(255) PRIMARY KEY REFERENCES users(email) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        speciality VARCHAR(100) NOT NULL,
        qualification VARCHAR(255),
        experience VARCHAR(50),
        hospital VARCHAR(255),
        country VARCHAR(100),
        state VARCHAR(100),
        city VARCHAR(100),
        postal_code VARCHAR(50),
        phone VARCHAR(50),
        fee VARCHAR(50),
        description TEXT
    );
    """)

    # 4. Consultations Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS consultations (
        id SERIAL PRIMARY KEY,
        patient_email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
        patient_name VARCHAR(255),
        symptoms TEXT NOT NULL,
        summary TEXT,
        urgency_level VARCHAR(50),
        recommended_specialty VARCHAR(100),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id SERIAL PRIMARY KEY,
        patient_email VARCHAR(255) REFERENCES users(email) ON DELETE CASCADE,
        doctor_email VARCHAR(255) REFERENCES doctors(email) ON DELETE CASCADE,
        date VARCHAR(50) NOT NULL,
        slot VARCHAR(50) NOT NULL,
        reason TEXT,
        status VARCHAR(50) DEFAULT 'Pending' CHECK(status IN ('Pending', 'Confirmed', 'Rejected', 'Completed')),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database tables verified & ready.")

# Initialize tables immediately on module load
init_db()