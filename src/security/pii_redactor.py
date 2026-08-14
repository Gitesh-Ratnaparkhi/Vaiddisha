# src/security/pii_redactor.py
import re

# Regex patterns for common PII
EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
PHONE_REGEX = r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
AADHAAR_SSN_REGEX = r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}\b|\b\d{3}-\d{2}-\d{4}\b"


def redact_pii_for_llm(symptoms_text: str) -> str:
  """Masks sensitive patient identifiers (emails, phone numbers, IDs) before sending to LLM."""
  if not symptoms_text:
    return ""

  redacted = re.sub(EMAIL_REGEX, "[REDACTED_EMAIL]", symptoms_text)
  redacted = re.sub(PHONE_REGEX, "[REDACTED_PHONE]", redacted)
  redacted = re.sub(AADHAAR_SSN_REGEX, "[REDACTED_ID]", redacted)

  return redacted