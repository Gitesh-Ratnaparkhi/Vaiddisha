# src/security/rate_limiter.py
from collections import defaultdict
import time


class SimpleRateLimiter:
  """In-memory rate limiter using a sliding window."""

  def __init__(self, max_requests: int = 15, window_seconds: int = 60):
    self.max_requests = max_requests
    self.window_seconds = window_seconds
    self.requests = defaultdict(list)

  def is_allowed(self, user_key: str) -> bool:
    """Returns True if the request is within rate limits; False if exceeded."""
    now = time.time()
    cutoff = now - self.window_seconds

    # Filter out requests older than window
    timestamps = [t for t in self.requests[user_key] if t > cutoff]
    self.requests[user_key] = timestamps

    if len(timestamps) < self.max_requests:
      self.requests[user_key].append(now)
      return True
    return False


# Global limiters for different actions
auth_rate_limiter = SimpleRateLimiter(max_requests=5, window_seconds=60)
llm_rate_limiter = SimpleRateLimiter(max_requests=10, window_seconds=60)