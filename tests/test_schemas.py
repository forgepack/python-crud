from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.enum.permission_action import EnumPermissionAction
from app.schemas.base import DTOMixinAudit
from app.schemas.role import DTORoleCreate
from app.schemas.user import DTOUserCreate


def test_role_create_rejects_duplicate_permission_ids() -> None:
    permission_id = uuid4()

    with pytest.raises(ValidationError, match="Duplicate permissions not allowed"):
        DTORoleCreate(name="Administrator", permission_ids=[permission_id, permission_id])


def test_user_create_normalizes_and_validates_a_valid_payload() -> None:
    user = DTOUserCreate(
        username="  alice  ",
        email="alice@example.com",
        password="SecurePassword1!",
        first_name=" Alice ",
        last_name=" Smith ",
    )

    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.first_name == "Alice"
    assert user.last_name == "Smith"


def test_permission_action_serializes_as_its_api_value() -> None:
    assert EnumPermissionAction.CREATE.value == "create"
    assert str(EnumPermissionAction.CREATE) == "create"


def test_audit_schema_serializes_uuid_and_datetime_as_json_values() -> None:
    identifier = uuid4()
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)
    audit = DTOMixinAudit(id=identifier, created_at=timestamp, updated_at=timestamp)

    assert audit.model_dump(mode="json") == {
        "id": str(identifier),
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "created_by": None,
        "updated_by": None,
        "version_id": 1,
    }
