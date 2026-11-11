from uuid import uuid4

import pytest
from pydantic import BaseModel

from app.services.base import ServiceBase, ServiceError


class Item:
    id = "id"

    def __init__(self) -> None:
        self.created_by = None
        self.updated_by = None


class ItemResponse(BaseModel):
    id: str


class EmptyQuery:
    def filter(self, *_args: object) -> "EmptyQuery":
        return self

    def first(self) -> None:
        return None


class EmptySession:
    def query(self, _model: type[Item]) -> EmptyQuery:
        return EmptyQuery()


def test_service_applies_audit_fields_to_new_instance() -> None:
    service = ServiceBase(Item, EmptySession(), ItemResponse)
    instance = Item()
    user_id = uuid4()

    result = service._apply_audit_fields(instance, user_id)

    assert result is instance
    assert instance.created_by == user_id
    assert instance.updated_by == user_id


def test_service_returns_not_found_domain_error_for_missing_instance() -> None:
    service = ServiceBase(Item, EmptySession(), ItemResponse)

    with pytest.raises(ServiceError, match="Item with id .* not found") as error:
        service.get(uuid4())

    assert error.value.code == "not_found"
