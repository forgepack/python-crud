from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_application_initializes() -> None:
    with TestClient(app) as application_client:
        response = application_client.get("/openapi.json")

    assert response.status_code == 200

    openapi = response.json()

    assert openapi["openapi"].startswith("3.")
    assert isinstance(openapi["info"]["title"], str)
    assert openapi["info"]["title"].strip()
    assert "/" in openapi["paths"]
    assert "/health" in openapi["paths"]


def test_root_endpoint_returns_expected_response() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome Fast API by Gadelha TI", "status": "success"}


def test_health_endpoint_returns_expected_response() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
