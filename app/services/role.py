import logging
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role
from app.schemas.role import DTORoleCreate, DTORoleRetrieve, DTORoleUpdate
from app.services.base import ServiceBase, ServiceError
from app.validations.validation import Validation

logger = logging.getLogger(__name__)


class ServiceRole(ServiceBase[Role, DTORoleCreate, DTORoleUpdate, DTORoleRetrieve]):
    """Role service with additional role-specific methods"""

    def __init__(self, db: Session):
        super().__init__(Role, db, DTORoleRetrieve)

    def get_default_roles(self, include_deleted: bool = False) -> list[DTORoleRetrieve]:
        """Get all default roles"""
        query = self.db.query(self.model).filter(self.model.is_default.is_(True))
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        return [self._to_response_dto(instance) for instance in query.all()]

    def update_permissions(
        self, role_id: UUID, permission_ids: list[UUID], current_user_id: UUID | None = None
    ) -> DTORoleRetrieve:
        """Update role permissions"""
        if len(permission_ids) > Validation.MAX_PERMISSIONS_PER_ROLE:
            raise ServiceError(
                f"A role cannot have more than {Validation.MAX_PERMISSIONS_PER_ROLE} permissions"
            )
        if len(permission_ids) != len(set(permission_ids)):
            raise ServiceError("Duplicate permissions are not allowed.")

        role = self._get_instance(role_id)
        if not role:
            raise ServiceError(f"Role with id {role_id} not found", code="not_found")

        permissions = self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
        if len(permissions) != len(permission_ids):
            found_ids = {str(perm.id) for perm in permissions}
            missing_ids = [str(pid) for pid in permission_ids if pid not in found_ids]
            raise ServiceError(
                f"Some permissions not found: {', '.join(missing_ids)}",
                code="permissions_not_found",
            )

        try:
            role.permissions = permissions
            if hasattr(role, "updated_by"):
                role.updated_by = current_user_id
            self.db.commit()
            self.db.refresh(role)
            return self._to_response_dto(role)
        except Exception as e:
            self._handle_exception(e, "update role permissions")
