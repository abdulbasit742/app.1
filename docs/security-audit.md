# Changed-area security audit — 2026-07-15

## Fixed

- Removed the hardcoded Flask signing secret.
- Removed automatic predictable administrator creation and printed credentials.
- Replaced wildcard credentialed CORS with exact origin configuration.
- Prevented public registration from assigning the administrator role.
- Added password, email, role, and text validation.
- Added bounded login failures and session rotation after successful login.
- Restricted member profile reads to self or administrator.
- Moved SQLite runtime data to the untracked Flask instance directory.
- Added JSON/body/origin checks, secure cookie defaults, API no-store behavior, and baseline security headers.
- Replaced raw internal exception responses on authentication/user routes.
- Added tests, source scanning, compile checks, and application-factory CI.

## Residual risks

- The in-memory login limiter is not shared across workers or hosts.
- Existing product, service, announcement, and contact routes retain legacy validation/error patterns.
- `db.create_all()` is not a migration system; schema evolution needs a migration tool before production use.
- A real production deployment needs HTTPS termination, a production WSGI server, centralized logs, backups, and monitoring.
- The React source is absent, so the compiled browser bundle remains only partially auditable.
