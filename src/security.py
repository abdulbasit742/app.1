import re
import time
from collections import defaultdict, deque
from urllib.parse import urlsplit

_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
_ALLOWED_ROLES = frozenset({"admin", "member"})


def normalize_email(value):
    email = str(value or "").strip().lower()
    if len(email) > 254 or not _EMAIL_RE.fullmatch(email):
        raise ValueError("A valid email address is required")
    return email


def validate_password(value):
    password = str(value or "")
    if len(password) < 12 or len(password) > 128:
        raise ValueError("Password must contain 12 to 128 characters")
    if not any(ch.isalpha() for ch in password) or not any(ch.isdigit() for ch in password):
        raise ValueError("Password must contain at least one letter and one number")
    return password


def clean_text(value, field, *, minimum=0, maximum=200):
    text = " ".join(str(value or "").replace("\x00", "").split()).strip()
    if len(text) < minimum:
        raise ValueError(f"{field} is required")
    if len(text) > maximum:
        raise ValueError(f"{field} must be {maximum} characters or fewer")
    return text


def normalize_role(value, *, public_registration=False):
    if public_registration:
        return "member"
    role = str(value or "member").strip().lower()
    if role not in _ALLOWED_ROLES:
        raise ValueError("Role must be admin or member")
    return role


def normalize_origin(value):
    parsed = urlsplit(str(value or "").strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("CORS origins must be explicit HTTP(S) origins")
    if parsed.path not in {"", "/"} or parsed.query or parsed.fragment or str(value).strip() == "*":
        raise ValueError("CORS origins cannot contain paths, queries, fragments, or wildcards")
    return f"{parsed.scheme}://{parsed.netloc}"


def parse_origins(value, *, port=5000):
    entries = [entry.strip() for entry in str(value or "").split(",") if entry.strip()]
    if not entries:
        entries = [f"http://localhost:{port}", f"http://127.0.0.1:{port}"]
    origins = []
    for entry in entries:
        origin = normalize_origin(entry)
        if origin not in origins:
            origins.append(origin)
    return tuple(origins)


def origin_allowed(origin, allowed_origins):
    if not origin:
        return True
    try:
        return normalize_origin(origin) in allowed_origins
    except ValueError:
        return False


class AttemptLimiter:
    def __init__(self, *, max_failures=5, window_seconds=900, block_seconds=900, clock=time.monotonic):
        self.max_failures = max_failures
        self.window_seconds = window_seconds
        self.block_seconds = block_seconds
        self.clock = clock
        self._failures = defaultdict(deque)
        self._blocked_until = {}

    def check(self, key):
        now = self.clock()
        blocked_until = self._blocked_until.get(key, 0)
        if blocked_until > now:
            return False, max(1, int(blocked_until - now))
        self._blocked_until.pop(key, None)
        queue = self._failures[key]
        while queue and queue[0] <= now - self.window_seconds:
            queue.popleft()
        return True, 0

    def failure(self, key):
        now = self.clock()
        queue = self._failures[key]
        queue.append(now)
        while queue and queue[0] <= now - self.window_seconds:
            queue.popleft()
        if len(queue) >= self.max_failures:
            self._blocked_until[key] = now + self.block_seconds
            queue.clear()
        return self.check(key)

    def success(self, key):
        self._failures.pop(key, None)
        self._blocked_until.pop(key, None)
