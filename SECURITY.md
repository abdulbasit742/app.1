# Security Policy

## Supported baseline

The maintained backend is the Flask application under `src/`. The committed frontend is a compiled artifact; its original source is not currently available for security review.

## Required deployment controls

- Configure a unique `SECRET_KEY` of at least 32 characters.
- Use HTTPS and set `SESSION_COOKIE_SECURE=true` outside local HTTP development.
- Restrict `CORS_ORIGINS` to exact trusted application origins.
- Keep SQLite/database files, environment values, logs, and backups outside Git.
- Remove one-time administrator bootstrap variables immediately after use.
- Place internet deployments behind rate limiting, monitoring, backups, and a production WSGI server.

## Reporting

Do not include credentials, session cookies, personal member data, or database files in a vulnerability report. Describe the affected route, expected behavior, observed behavior, and a minimal synthetic reproduction.

## Known limitations

- Login throttling is in-process and resets when the application restarts; a shared limiter is required for multi-worker deployments.
- SQLite is appropriate for local/small deployments, not high-concurrency multi-instance operation.
- Other legacy CRUD routes still need the same structured validation and sanitized error handling now applied to authentication and user management.
- The compiled frontend cannot be reliably patched or audited without its source project.
