# PES Pakistan Entrepreneurship Society Web Application

A Flask + SQLite application serving the committed React/Vite static build for member management, products, services, announcements, and contact messages.

## Security baseline

- Flask application factory with environment-driven configuration
- signed HttpOnly session cookies with `SameSite=Lax`
- exact CORS origin allowlist; wildcards are rejected
- public registration always creates a `member`, never an administrator
- login attempt throttling and session rotation after authentication
- administrator creation only through explicit one-time environment variables
- members may read only their own profile; administrators manage other users
- bounded JSON request bodies, same-origin mutation checks, and API security headers
- SQLite runtime data stored under the untracked `instance/` directory

## Setup

Requirements: Python 3.10 or newer.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Copy the variable names from `.env.example` into your shell or deployment secret manager. The application does not automatically load `.env` files.

Required:

```text
SECRET_KEY=<random value of at least 32 characters>
```

Optional first-administrator bootstrap:

```text
PES_BOOTSTRAP_ADMIN_EMAIL=<administrator email>
PES_BOOTSTRAP_ADMIN_PASSWORD=<unique password of at least 12 characters with letters and numbers>
PES_BOOTSTRAP_ADMIN_NAME=<display name>
```

Start the application once, verify the administrator exists, then remove the bootstrap variables. No default account or password is created.

Run locally:

```bash
python src/main.py
```

The default bind address is `127.0.0.1:5000`. Set `BIND_HOST=0.0.0.0` only behind an authenticated HTTPS deployment boundary. Set `SESSION_COOKIE_SECURE=true` in HTTPS deployments.

## Verification

```bash
python -m unittest discover -s tests -v
python scripts/security_check.py
python -m compileall -q src tests scripts
```

CI additionally installs the pinned dependencies and smoke-tests the application factory against an in-memory SQLite database on Python 3.10 and 3.12.

## API boundary

Authentication uses Flask's signed server-side session cookie contract, not JWTs. Browser mutation requests must use `application/json`; credentialed cross-origin requests are accepted only from `CORS_ORIGINS`.

Public endpoints include registration, login, product/service/announcement reads, contact submission, and health status. Administrative writes remain protected by `admin_required`.

## Current frontend limitation

The repository contains the compiled static frontend but not its original React source. Backend behavior can be maintained and tested here, but UI source changes require recovering and committing the original frontend project rather than editing minified bundles.

## Documentation

- [Security policy](SECURITY.md)
- [Reference review](docs/reference-review.md)
- [Changed-area security audit](docs/security-audit.md)
