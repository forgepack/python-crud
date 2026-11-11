# Contributing to python-template

Thank you for contributing to this FastAPI template. This guide describes the local setup, quality checks, and pull request expectations.

## Prerequisites

- Python 3.13, 3.14, or 3.15
- Git

## Local setup

Fork the repository and create a branch from `main`:

```bash
git checkout main
git pull origin main
git checkout -b feat/short-description
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install the project and its development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Configure the database in `.env`:

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

Run the application:

```bash
python -m app.main
```

For a quick start, see [QUICKSTART.md](./QUICKSTART.md). For full API documentation, see [ENDPOINTS.md](./ENDPOINTS.md).

## Quality checks

Run every command below before opening a pull request:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -v
```

To automatically fix lint and formatting issues:

```bash
python -m ruff check . --fix
python -m ruff format .
```

To inspect test coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

The GitHub Actions workflow runs Ruff linting, formatting verification, and the test suite for each push and pull request.

## Code standards

- Use Python 3.13-compatible syntax and keep code compatible with the supported Python range declared in `pyproject.toml`.
- Follow the Ruff configuration in `pyproject.toml`; it is the source of truth for linting and formatting.
- Add type annotations to new public functions and methods.
- Keep HTTP routes in `app/routers/`, business rules in `app/services/`, persistence code in `app/repositories/`, and request/response models in `app/schemas/` as the application grows.
- Add or update tests for every behavior change.
- Update the README and relevant documentation when public behavior, configuration, or setup instructions change.

## Commit conventions

Use Conventional Commits:

```text
<type>(<scope>): <description>
```

| Type | Use |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Documentation change |
| `style` | Formatting-only change |
| `refactor` | Code restructuring without behavior changes |
| `perf` | Performance improvement |
| `test` | Test creation or update |
| `build` | Dependency or packaging change |
| `ci` | Continuous integration change |
| `chore` | Other maintenance work |

Examples:

```text
feat(health): add readiness endpoint
fix(config): read the application port from the environment
test(api): cover invalid health response
ci(quality): run Ruff checks
```

## Pull requests

Before opening a pull request:

1. Rebase or merge the current `main` branch into your feature branch.
2. Verify that linting, formatting, and tests pass locally.
3. Describe the behavior change and how you validated it.
4. Link related issues, when applicable.
5. Keep the pull request focused; avoid unrelated formatting or refactors.

Maintainers may request changes before approving a pull request.

## Suggesting features

Feature requests should include:

- The use case and expected benefit.
- Acceptance criteria describing the desired behavior.
- Any relevant API, configuration, or compatibility considerations.
