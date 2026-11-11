<div align="center">

# _Python Template_

[![GitHub stars](https://img.shields.io/github/stars/forgepack/python-template?style=social)](https://github.com/forgepack/python-template)
[![GitHub forks](https://img.shields.io/github/forks/forgepack/python-template?style=social)](https://github.com/forgepack/python-template/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/forgepack/python-template?style=social)](https://github.com/forgepack/python-template)

[![CI](https://github.com/forgepack/python-template/actions/workflows/ci.yml/badge.svg)](https://github.com/forgepack/python-template/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/forgepack/python-template/blob/main/LICENSE.md)

</div>

Reusable Python application template built with FastAPI.

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.13%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)

## 📖 Interactive API Documentation

The API includes automatic interactive documentation powered by **Swagger UI** and **OpenAPI**:

- **Swagger UI** (Interactive): http://127.0.0.1:9001/docs
- **ReDoc** (Alternative): http://127.0.0.1:9001/redoc
- **OpenAPI Schema**: http://127.0.0.1:9001/openapi.json

### Key Endpoints

**Public (no auth required):**
- `GET /health` - Health check
- `GET /` - Welcome message
- `POST /user/login` - Authenticate and get JWT token
- `POST /admin/init/create-first-user` - Create first user (database initialization)

**Protected (requires JWT Bearer token):**
- `POST /user/` - Create user
- `GET /user/` - List users
- `GET /user/{id}` - Get user by ID
- `PUT /user/` - Update user
- `DELETE /user/{id}` - Delete user
- `GET /role/`, `POST /role/`, `PUT /role/`, `DELETE /role/{id}` - Role management
- `GET /permissions/`, `DELETE /permissions/{id}` - Permission management

**Documentation:**
- [SWAGGER_GUIDE.md](./SWAGGER_GUIDE.md) - Complete Swagger UI tutorial
- [SWAGGER_INTEGRATION.md](./SWAGGER_INTEGRATION.md) - OpenAPI integration details
- [ENDPOINTS.md](./ENDPOINTS.md) - cURL examples for all endpoints

## Configuration
### _Windows PowerShell_
```bash
Copy-Item .env.example .env
```
### _Linux_
```bash
cp .env.example .env
```

## Development

This project requires Python 3.13 or later.

```bash
# create virtual environment
# Windows PowerShell
py -3.13 -m venv .venv
# Linux
python3.13 -m venv .venv

# activate virtual environment (*)
# Windows PowerShell
.venv/Scripts/activate
# Linux
source .venv/bin/activate

# update pip
python -m pip install --upgrade pip

# install dependencies
python -m pip install -e ".[dev]"

# generate the artifacts
python -m build

# inspect the contents of the wheel
python -m zipfile -l dist/python_template-1.0.0-py3-none-any.whl

# run application (*)
python -m app.main
```

## Ruff linter formatting

```bash
# automatically formats the code to follow the standard
python -m ruff format .

# checks whether the code follows the formatting standard
python -m ruff format --check .

# automatic correction
ruff check --fix .

# identifies linting issues and potential code errors
python -m ruff check .
```

## Running Tests

```bash
# test coverage verification
python -m pytest --cov=app --cov-report=term-missing

# test report, in /htmlcov/index.html
python -m pytest --cov=app --cov-report=html

# test execution, with details
python -m pytest -v
```

## DEVELOPERS

### Contributors
> _[Gadelha TI](https://github.com/gadelhati)_ - *Research Software Engineer · Software Architect · Lead Developer*

## LICENSE

This project is licensed under the __MIT License__ - see the [MIT LICENSE](https://choosealicense.com/licenses/mit/) file for details.

<div align="center">

__⭐ Did you like the project? Leave a star! ⭐__

[![GitHub stars](https://img.shields.io/github/stars/forgepack/python-template?style=social)](https://github.com/forgepack/python-template)
[![GitHub forks](https://img.shields.io/github/forks/forgepack/python-template?style=social)](https://github.com/forgepack/python-template/fork)
[![GitHub watchers](https://img.shields.io/github/watchers/forgepack/python-template?style=social)](https://github.com/forgepack/python-template)

__Made by [Forgepack](https://github.com/forgepack)__

</div>