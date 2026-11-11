from sqlalchemy.orm import Session

from app.enum.permission_action import EnumPermissionAction
from app.models.permission import Permission
from app.schemas.permission import DTOPermissionRetrieve
from app.services.base import ServiceBase


class ServicePermission(ServiceBase[Permission, None, None, DTOPermissionRetrieve]):
    """Permission service (read-only)"""

    def __init__(self, db: Session):
        super().__init__(Permission, db, DTOPermissionRetrieve)

    def get_by_action(
        self, action: EnumPermissionAction, include_deleted: bool = False
    ) -> list[DTOPermissionRetrieve]:
        """Get permissions by enum action"""
        query = self.db.query(self.model).filter(self.model.action == action.value)
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        return [self._to_response_dto(instance) for instance in query.all()]

    def sync_with_enum(self) -> None:
        """Ensure all enum values exist in the DB (idempotent)."""
        existing_actions = {p.action for p in self.db.query(self.model).all()}
        for action in EnumPermissionAction:
            if action.value not in existing_actions:
                self.db.add(Permission(action=action.value))
        self.db.commit()
