import httpx


def test_health(client: httpx.Client) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_home(client: httpx.Client) -> None:
    response = client.get("/")

    assert response.status_code == 200


def test_login_returns_token(token: str) -> None:
    assert token


def test_list_users(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/user/", headers=auth_headers)

    assert response.status_code == 200


def test_list_permissions(client: httpx.Client, auth_headers: dict[str, str]) -> None:
    response = client.get("/permissions/", headers=auth_headers)

    assert response.status_code == 200
