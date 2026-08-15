# src/security/hashing.py
import hashlib
import os
import secrets


def hash_password(password: str) -> str:
  """Hashes a password using PBKDF2 HMAC SHA-256 with a random salt."""
  if not password or len(password) < 8:
    raise ValueError("Password must be at least 8 characters long.")

  salt = secrets.token_hex(16)
  pwd_hash = hashlib.pbkdf2_hmac(
      "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000
  ).hex()
  return f"{salt}${pwd_hash}"


def verify_password(plain_password: str, hashed_value: str | bytes) -> bool:
  """Verifies a plain password against the stored salt$hash string."""
  if not plain_password or not hashed_value:
    return False

  if isinstance(hashed_value, bytes):
    try:
      hashed_value = hashed_value.decode("utf-8")
    except UnicodeDecodeError:
      return False

  if hashed_value.startswith(("$2a$", "$2b$", "$2y$")):
    try:
      import bcrypt
      return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_value.encode("utf-8"))
    except Exception:
      return False

  if "$" not in hashed_value:
    return False

  try:
    salt, stored_hash = hashed_value.split("$", 1)
    new_hash = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()
    return secrets.compare_digest(stored_hash, new_hash)
  except Exception:
    return False