import csv
import re
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]
CSV_PATH = BACKEND_DIR / "data" / "nagpur_specialists.csv"
CSV_COLUMNS = [
    "Doctor_id", "Name", "Speciality", "Qualification", "Experience",
    "Hospital", "Area", "City", "Phone", "Fee", "Rating", "Email",
    "Country", "State", "Pincode", "Description",
]


def append_registered_doctor(
    *,
    email: str,
    name: str,
    speciality: str,
    qualification: str,
    experience: str,
    hospital: str,
    country: str,
    state: str,
    city: str,
    postal_code: str,
    phone: str,
    fee: str,
    description: str,
) -> None:
    """Append a newly registered doctor to the directory CSV once."""
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    if CSV_PATH.exists() and CSV_PATH.stat().st_size > 0:
        with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.DictReader(file))

    clean_email = email.strip().lower()
    if any((row.get("Email") or "").strip().lower() == clean_email for row in rows):
        return

    ids = []
    for row in rows:
        match = re.fullmatch(r"D(\d+)", (row.get("Doctor_id") or "").strip())
        if match:
            ids.append(int(match.group(1)))
    doctor_id = f"D{max(ids, default=0) + 1:03d}"

    new_row = {
        "Doctor_id": doctor_id,
        "Name": name.strip(),
        "Speciality": speciality.strip(),
        "Qualification": qualification.strip(),
        "Experience": experience.strip(),
        "Hospital": hospital.strip(),
        "Area": "",
        "City": city.strip(),
        "Phone": phone.strip(),
        "Fee": fee.strip(),
        "Rating": "",
        "Email": clean_email,
        "Country": country.strip(),
        "State": state.strip(),
        "Pincode": postal_code.strip(),
        "Description": description.strip(),
    }

    write_header = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
    with CSV_PATH.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        if write_header:
            writer.writeheader()
        writer.writerow(new_row)