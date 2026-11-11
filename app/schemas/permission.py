from __future__ import annotations

from app.enum.permission_action import EnumPermissionAction
from app.schemas.base import DTOMixinAudit, DTOPagination, DTOSoftDeleteMixin


class DTOPermissionRetrieve(DTOMixinAudit, DTOSoftDeleteMixin):
    """DTO for permission response"""

    name: str
    description: str | None = None
    action: EnumPermissionAction


class DTOPermissionRetrieveAll(DTOPagination):
    """DTO for permission list response with pagination"""

    items: list[DTOPermissionRetrieve]


# Rebuild models to resolve forward references in circular relationships
DTOPermissionRetrieve.model_rebuild()
DTOPermissionRetrieveAll.model_rebuild()
