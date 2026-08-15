# src/security/sanitizer.py
import html
import re


def sanitize_text(user_input: str, max_length: int = 2000) -> str:
  """Sanitizes user input by escaping HTML tags and stripping control characters."""
  if not user_input:
    return ""

  # Truncate overly long payloads to avoid resource exhaustion
  cleaned = user_input.strip()[:max_length]

  # Escape HTML entities (<script>, <iframe>, etc.)
  cleaned = html.escape(cleaned)

  # Remove dangerous null bytes or invisible control characters (keep regular whitespace)
  cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", cleaned)

  return cleaned


def is_potential_prompt_injection(text: str) -> bool:
  """Detects common prompt injection patterns attempting to override clinical behavior."""
  patterns = [
      r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
      r"you\s+are\s+now\s+(unrestricted|DAN|jailbroken)",
      r"system\s*:\s*override",
      r"disregard\s+the\s+medical\s+guidelines",
  ]
  lower_text = text.lower()
  return any(re.search(pat, lower_text) for pat in patterns)