from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.permission import get_permission_service, permission
from app.services.base import ServiceError


class PermissionServiceStub:
    def list(self, **_kwargs: object) -> dict[str, object]:
        return {
            "items": [],
            "pagination": {
                "total": 0,
                "page": 1,
                "limit": 20,
                "total_pages": 0,
                "has_next": False,
                "has_prev": False,
            },
        }

    def get(self, _permission_id: object, **_kwargs: object) -> object:
        raise ServiceError("Permission not found", code="not_found")

    def sync_with_enum(self) -> None:
        return None


def create_client() -> TestClient:
    app = FastAPI()
    app.include_router(permission)
    app.dependency_overrides[get_permission_service] = PermissionServiceStub
    return TestClient(app)


def test_list_permissions_returns_paginated_contract() -> None:
    response = create_client().get("/permissions/")

    assert response.status_code == 200
    assert response.json()["pagination"]["total"] == 0


def test_get_permission_returns_not_found_for_missing_resource() -> None:
    response = create_client().get(f"/permissions/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Permission not found"}


def test_sync_permissions_returns_success_message() -> None:
    response = create_client().post("/permissions/sync")

    assert response.status_code == 200
    assert response.json() == {"message": "Permissions synchronized successfully"}
