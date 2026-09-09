"""Import a validated specialist CSV into the PostgreSQL doctors directory."""
import csv
import sys
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from src.repositories.database import get_db_connection, init_db  # noqa: E402

CSV_PATH = BACKEND_DIR / "data" / "nagpur_specialists.csv"
REQUIRED_COLUMNS = {
    "Doctor_id", "Name", "Speciality", "Qualification", "Experience",
    "Hospital", "Area", "City", "Phone", "Fee", "Rating", "Email",
    "Country", "State", "Pincode", "Description",
}


def clean(value: str) -> str:
    return value.strip()


def read_rows() -> list[dict[str, str]]:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")
        rows = [{key: clean(value or "") for key, value in row.items()} for row in reader]

    if not rows:
        raise ValueError("The CSV does not contain any specialist rows.")

    duplicate_ids = sorted({
        row["Doctor_id"] for row in rows
        if row["Doctor_id"] and sum(r["Doctor_id"] == row["Doctor_id"] for r in rows) > 1
    })
    duplicate_emails = sorted({
        row["Email"].lower() for row in rows
        if row["Email"] and sum(r["Email"].lower() == row["Email"].lower() for r in rows) > 1
    })
    if duplicate_ids or duplicate_emails:
        problems = []
        if duplicate_ids:
            problems.append(f"duplicate Doctor_id values: {', '.join(duplicate_ids)}")
        if duplicate_emails:
            problems.append(f"duplicate Email values: {', '.join(duplicate_emails)}")
        raise ValueError("; ".join(problems))

    for row in rows:
        for field in ("Doctor_id", "Name", "Speciality", "Email", "City"):
            if not row[field]:
                raise ValueError(f"{field} is empty for a CSV row.")
        try:
            if row["Rating"]:
                float(row["Rating"])
            if row["Fee"]:
                float(row["Fee"])
        except ValueError as error:
            raise ValueError(f"Fee and Rating must be numeric for {row['Doctor_id']}.") from error

    return rows


def import_rows(rows: list[dict[str, str]]) -> None:
    init_db()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            for row in rows:
                email = row["Email"].lower()
                cursor.execute(
                    """
                    INSERT INTO users (email, password_hash, role, terms_accepted)
                    VALUES (%s, %s, 'Doctor', TRUE)
                    ON CONFLICT (email) DO NOTHING
                    """,
                    (email, "directory-import-no-login"),
                )
                cursor.execute(
                    """
                    INSERT INTO doctors (
                        email, name, speciality, qualification, experience, hospital,
                        country, state, city, postal_code, phone, fee, description,
                        doctor_id, area, rating
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO UPDATE SET
                        name = EXCLUDED.name,
                        speciality = EXCLUDED.speciality,
                        qualification = EXCLUDED.qualification,
                        experience = EXCLUDED.experience,
                        hospital = EXCLUDED.hospital,
                        country = EXCLUDED.country,
                        state = EXCLUDED.state,
                        city = EXCLUDED.city,
                        postal_code = EXCLUDED.postal_code,
                        phone = EXCLUDED.phone,
                        fee = EXCLUDED.fee,
                        description = EXCLUDED.description,
                        doctor_id = EXCLUDED.doctor_id,
                        area = EXCLUDED.area,
                        rating = EXCLUDED.rating
                    """,
                    (
                        email, row["Name"], row["Speciality"], row["Qualification"],
                        row["Experience"], row["Hospital"], row["Country"], row["State"],
                        row["City"], row["Pincode"], row["Phone"], row["Fee"], row["Description"],
                        row["Doctor_id"], row["Area"], row["Rating"] or None,
                    ),
                )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    load_dotenv(BACKEND_DIR / ".env")
    specialist_rows = read_rows()
    print(f"Validated {len(specialist_rows)} specialist rows.")
    import_rows(specialist_rows)
    print("Specialist import completed successfully.")