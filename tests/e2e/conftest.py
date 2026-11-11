import os

import httpx
import pytest

BASE_URL = os.getenv("E2E_BASE_URL", "http://127.0.0.1:9001")
USERNAME = os.getenv("E2E_USERNAME", "admin")
PASSWORD = os.getenv("E2E_PASSWORD", "Admin@123456")
EMAIL = os.getenv("E2E_EMAIL", "admin@example.com")


@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE_URL, timeout=10) as http:
        try:
            http.get("/health")
        except httpx.TransportError:
            pytest.skip(f"Servidor e2e indisponível em {BASE_URL}", allow_module_level=True)
        yield http


@pytest.fixture(scope="session")
def token(client: httpx.Client) -> str:
    client.post(
        "/admin/init/create-first-user",
        json={
            "username": USERNAME,
            "email": EMAIL,
            "password": PASSWORD,
            "full_name": "Administrator",
        },
    )  # 201 criado ou 403 já inicializado: ambos são aceitáveis

    response = client.post("/user/login", json={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200, response.text

    data = response.json()
    access_token = data.get("access_token") or data.get("validationErrors", {}).get("access_token")
    assert access_token, f"Token não encontrado na resposta: {data}"
    return access_token


@pytest.fixture
def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
