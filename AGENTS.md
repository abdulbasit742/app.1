# AGENTS.md

## Scope

These instructions apply to the entire `abdulbasit742/app.1` repository.

Project: PES Pakistan Entrepreneurship Society Flask application. The original React source is not committed; `src/static/` is a generated browser build and must not be hand-edited.

## Architecture

- `src/main.py`: application factory, blueprints, security headers, static serving
- `src/config.py`: environment and bootstrap configuration
- `src/security.py`: dependency-free validation and rate-limit policy
- `src/routes/`: HTTP authorization and CRUD boundaries
- `src/models/user.py`: SQLAlchemy models
- `instance/`: untracked SQLite/runtime data
- `tests/`: dependency-free policy and source-contract tests

## Working rules

1. Never reintroduce default credentials, a hardcoded `SECRET_KEY`, wildcard credentialed CORS, public role selection, or `debug=True`.
2. Keep public registration fixed to the `member` role; administrator creation is server-controlled only.
3. Validate JSON inputs, bound field sizes, roll back failed writes, and do not return raw internal exceptions.
4. Re-check the active database user on protected requests; do not trust a role cached in the session.
5. Store local databases and secrets outside tracked source.
6. Do not edit minified files under `src/static/`; recover the original frontend source for UI work.

## Verification

```bash
python -m unittest discover -s tests -v
python scripts/security_check.py
python -m compileall -q src tests scripts
```

With dependencies installed and a temporary secret configured, also smoke-test `create_app` as documented in CI.
