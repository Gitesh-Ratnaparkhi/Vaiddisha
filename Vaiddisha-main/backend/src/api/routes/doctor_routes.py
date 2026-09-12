# backend/src/api/routes/doctor_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from src.repositories.database import get_db_connection

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/search")
def search_doctors(
    speciality: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    postal_code: Optional[str] = Query(None)
):
    from psycopg2.extras import RealDictCursor
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Query without the non-existent 'id' and 'rating' columns
    query = """
<<<<<<< HEAD
        SELECT name, email, speciality, qualification, experience, hospital,
               country, state, city, postal_code, phone, fee, description
=======
         SELECT doctor_id, name, email, speciality, qualification, experience, hospital,
             area, country, state, city, postal_code, phone, fee, rating, description
>>>>>>> 57e9732 (Final commit after PP2)
        FROM doctors
        WHERE 1=1
    """
    params = []

    # 1. Speciality search
    if speciality and speciality.strip():
        query += " AND speciality ILIKE %s"
        params.append(f"%{speciality.strip()}%")

    # 2. General Location search bar
    if location and location.strip():
        loc = f"%{location.strip()}%"
        query += " AND (city ILIKE %s OR state ILIKE %s OR country ILIKE %s OR postal_code ILIKE %s)"
        params.extend([loc, loc, loc, loc])

    # 3. Granular Location Filters
    if country and country.strip():
        query += " AND country ILIKE %s"
        params.append(f"%{country.strip()}%")

    if state and state.strip():
        query += " AND state ILIKE %s"
        params.append(f"%{state.strip()}%")

    if city and city.strip():
        query += " AND city ILIKE %s"
        params.append(f"%{city.strip()}%")

    if postal_code and postal_code.strip():
        query += " AND postal_code ILIKE %s"
        params.append(f"%{postal_code.strip()}%")

<<<<<<< HEAD
    query += " ORDER BY name ASC LIMIT 50;"
=======
    query += " ORDER BY rating DESC NULLS LAST, name ASC LIMIT 50;"
>>>>>>> 57e9732 (Final commit after PP2)

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    # Format return list (using email as key/identifier)
    doctors_list = []
    for idx, row in enumerate(rows):
        doctors_list.append({
            "id": row.get("email") or str(idx + 1),
<<<<<<< HEAD
=======
            "doctor_id": row.get("doctor_id") or "",
>>>>>>> 57e9732 (Final commit after PP2)
            "name": row.get("name") or "Doctor",
            "email": row.get("email"),
            "speciality": row.get("speciality") or "General Physician",
            "qualification": row.get("qualification") or "MBBS",
            "experience": row.get("experience") or "5+ Years",
            "hospital": row.get("hospital") or "Private Practice",
<<<<<<< HEAD
=======
            "area": row.get("area") or "",
>>>>>>> 57e9732 (Final commit after PP2)
            "country": row.get("country") or "India",
            "state": row.get("state") or "",
            "city": row.get("city") or "",
            "postal_code": row.get("postal_code") or "",
            "phone": row.get("phone") or "",
            "fee": row.get("fee") or "₹500",
            "description": row.get("description") or "",
<<<<<<< HEAD
            "rating": row.get("rating") or 4.8
=======
            "rating": float(row["rating"]) if row.get("rating") is not None else None
>>>>>>> 57e9732 (Final commit after PP2)
        })

    return {"status": "success", "count": len(doctors_list), "doctors": doctors_list}