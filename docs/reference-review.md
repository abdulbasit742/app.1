# Reference review

## Pallets Flask tutorial

Adopted: application factory, instance-relative runtime data, configuration overrides for tests, and deployment secret replacement.

Not adopted: rewriting the existing application into the tutorial package structure.

## cookiecutter-flask

Adopted: environment-driven configuration, repeatable verification, and separation between source and runtime data.

Not adopted: replacing the current application with a generated project or adding its full dependency stack.

## Flask-AppBuilder

Adopted: authentication and role decisions remain server-owned and protected routes re-check the active database user.

Not adopted: migrating the existing PES data model and UI to a new admin framework.
