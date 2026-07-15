import os
from datetime import timedelta
from pathlib import Path

from src.security import normalize_email, parse_origins, validate_password


def _boolean(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def bootstrap_admin_from_env():
    email = os.getenv("PES_BOOTSTRAP_ADMIN_EMAIL", "").strip()
    password = os.getenv("PES_BOOTSTRAP_ADMIN_PASSWORD", "")
    name = os.getenv("PES_BOOTSTRAP_ADMIN_NAME", "PES Administrator").strip()
    if not email and not password:
        return None
    if not email or not password:
        raise RuntimeError("Both PES_BOOTSTRAP_ADMIN_EMAIL and PES_BOOTSTRAP_ADMIN_PASSWORD are required")
    return {"email": normalize_email(email), "password": validate_password(password), "name": name[:100] or "PES Administrator"}


def load_config(instance_path, overrides=None):
    overrides = overrides or {}
    testing = bool(overrides.get("TESTING", False))
    secret = overrides.get("SECRET_KEY") or os.getenv("SECRET_KEY")
    if not testing and (not secret or len(secret) < 32):
        raise RuntimeError("SECRET_KEY must be configured with at least 32 characters")
    secret = secret or "test-secret-key-that-is-long-enough"
    port = int(os.getenv("PORT", "5000"))
    database_uri = overrides.get("SQLALCHEMY_DATABASE_URI") or os.getenv("DATABASE_URL") or f"sqlite:///{Path(instance_path) / 'app.db'}"
    config = {
        "SECRET_KEY": secret,
        "SQLALCHEMY_DATABASE_URI": database_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "MAX_CONTENT_LENGTH": 64 * 1024,
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_SECURE": _boolean("SESSION_COOKIE_SECURE", False),
        "PERMANENT_SESSION_LIFETIME": timedelta(hours=12),
        "CORS_ORIGINS": parse_origins(os.getenv("CORS_ORIGINS"), port=port),
        "BOOTSTRAP_ADMIN": bootstrap_admin_from_env(),
    }
    config.update(overrides)
    return config
