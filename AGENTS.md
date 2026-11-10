# Project Guidelines

## Runtime and dependencies

- Support Python versions `>=3.13,<3.16`; use Python 3.13 locally unless a task requires another supported version.
- Declare production dependencies in `pyproject.toml` with compatible upper bounds.
- Install development tools with `python -m pip install -e ".[dev]"`.
- Store configuration in `app/config.py` using `pydantic-settings`; use the `UVICORN_` environment-variable prefix and do not commit `.env` files.

## Application structure

- Keep application startup and router registration in `app/main.py`.
- Add HTTP endpoints in `app/routers/`, request and response models in `app/schemas/`, business logic in `app/services/`, and persistence concerns in `app/repositories/`.
- Preserve `/health` as a lightweight liveness endpoint unless a task explicitly requires dependency readiness checks.

## Tests and quality

- Add or update pytest tests in `tests/` for every behavior change, including HTTP status codes and response payloads for endpoint changes.
- Ruff configuration in `pyproject.toml` is authoritative. Run `python -m ruff check .` and `python -m ruff format --check .`.
- Run `python -m pytest -v` after code changes. The CI workflow runs linting, formatting, and tests for Python 3.13 through 3.15.

## Documentation

- Update `README.md` when setup, supported Python versions, public endpoints, or configuration behavior changes.
- Follow `CONTRIBUTING.md` for local setup, commit conventions, and pull request expectations.