from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.schemas.base import BaseConfig, DTOMixinAudit, DTOPagination, DTOSoftDeleteMixin
from app.schemas.permission import DTOPermissionRetrieve
from app.validations.validation import Validation


class DTORoleCreate(BaseModel):
    """DTO for creating a role"""

    name: str
    description: str | None = None
    is_default: bool = False
    permission_ids: list[UUID] | None = Field(
        default=None, max_length=Validation.MAX_PERMISSIONS_PER_ROLE
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        result = Validation.validate_name(v, "Role name")
        if result is None:
            raise ValueError("Role name is required")
        return result

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        return Validation.validate_name(v, "Description")

    @field_validator("permission_ids")
    @classmethod
    def validate_permission_ids(cls, v: list[UUID] | None) -> list[UUID] | None:
        if v is None:
            return v
        if len(v) > Validation.MAX_PERMISSIONS_PER_ROLE:
            raise ValueError(
                f"A role cannot have more than {Validation.MAX_PERMISSIONS_PER_ROLE} permissions"
            )
        if len(v) != len(set(v)):
            raise ValueError("Duplicate permissions not allowed")
        return v

    model_config = BaseConfig.model_config


class DTORoleUpdate(BaseModel):
    """DTO for updating a role"""

    name: str | None = None
    description: str | None = None
    is_default: bool | None = None
    permission_ids: list[UUID] | None = Field(
        default=None, max_length=Validation.MAX_PERMISSIONS_PER_ROLE
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        return Validation.validate_name(v, "Role name")

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        return Validation.validate_name(v, "Description")

    @field_validator("permission_ids")
    @classmethod
    def validate_permission_ids(cls, v: list[UUID] | None) -> list[UUID] | None:
        if v is None:
            return v
        if len(v) > Validation.MAX_PERMISSIONS_PER_ROLE:
            raise ValueError(
                f"A role cannot have more than {Validation.MAX_PERMISSIONS_PER_ROLE} permissions"
            )
        if len(v) != len(set(v)):
            raise ValueError("Duplicate permissions not allowed")
        return v

    model_config = BaseConfig.model_config


class DTORoleRetrieve(DTOMixinAudit, DTOSoftDeleteMixin):
    """DTO for role response"""

    name: str
    description: str | None = None
    is_default: bool
    permissions: list[DTOPermissionRetrieve] = Field(default_factory=list)


class DTORoleRetrieveAll(DTOPagination):
    """DTO for role list response with pagination"""

    items: list[DTORoleRetrieve]


# Rebuild models to resolve forward references in circular relationships
DTORoleRetrieve.model_rebuild()
DTORoleRetrieveAll.model_rebuild()
