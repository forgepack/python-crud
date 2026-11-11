from typing import Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db  # Assuming you have this dependency
from app.schemas.role import DTORoleCreate, DTORoleRetrieve, DTORoleUpdate
from app.schemas.user import DTOUserRetrieve
from app.services.base import ServiceError
from app.services.role import ServiceRole
from app.services.user import ServiceUser

role = APIRouter(prefix="/role", tags=["role"])

security = HTTPBearer()


def get_role_service(db: Session = Depends(get_db)) -> ServiceRole:
    """Dependency to get role service instance"""
    return ServiceRole(db)


def get_user_service(db: Session = Depends(get_db)) -> ServiceUser:
    """Dependency to get user service instance"""
    return ServiceUser(db)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: ServiceUser = Depends(get_user_service),
) -> DTOUserRetrieve:
    """Dependency to get current authenticated user"""
    try:
        return service.get_current_user(credentials.credentials)
    except ServiceError as e:
        if e.code in ["invalid_token", "token_expired"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.message,
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
        raise HTTPException(status_code=400, detail=e.message) from e


# Pydantic models for request bodies
class PermissionUpdateRequest(BaseModel):
    permission_ids: list[UUID]


# CRUD endpoints
@role.post("/", response_model=DTORoleRetrieve, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: DTORoleCreate,
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Create a new role
    Requires authentication
    """
    try:
        return service.create(role_data, current_user_id=current_user.id)
    except ServiceError as e:
        if e.code == "integrity_error":
            raise HTTPException(status_code=409, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.get("/", response_model=dict[str, Any])
async def list_roles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    include_deleted: bool = Query(False, description="Include soft-deleted roles"),
    name: str | None = Query(None, description="Filter by role name"),
    is_default: bool | None = Query(None, description="Filter by default roles"),
    is_active: bool | None = Query(None, description="Filter by active status"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    List all roles with pagination and optional filters
    Requires authentication
    """
    try:
        filters = {}
        if name:
            filters["name"] = name
        if is_default is not None:
            filters["is_default"] = is_default
        if is_active is not None:
            filters["is_active"] = is_active

        result = service.list(page=page, limit=limit, include_deleted=include_deleted, **filters)
        return result
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.get("/defaults", response_model=list[DTORoleRetrieve])
async def get_default_roles(
    include_deleted: bool = Query(False, description="Include soft-deleted roles"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Get all default roles
    Requires authentication
    """
    try:
        return service.get_default_roles(include_deleted=include_deleted)
    except ServiceError as e:
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.get("/{role_id}", response_model=DTORoleRetrieve)
async def get_role(
    role_id: UUID = Path(..., description="Role ID"),
    include_deleted: bool = Query(False, description="Include soft-deleted roles"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Get a specific role by ID
    Requires authentication
    """
    try:
        return service.get(role_id, include_deleted=include_deleted)
    except ServiceError as e:
        if e.code == "not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.put("/{role_id}", response_model=DTORoleRetrieve)
async def update_role(
    role_id: UUID = Path(..., description="Role ID"),
    role_data: DTORoleUpdate = Body(...),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Update an existing role
    Requires authentication
    """
    try:
        return service.update(role_id, role_data, current_user_id=current_user.id)
    except ServiceError as e:
        if e.code == "not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        if e.code == "integrity_error":
            raise HTTPException(status_code=409, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.delete("/{role_id}")
async def delete_role(
    role_id: UUID = Path(..., description="Role ID"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Hard delete a role (permanently remove from database)
    Requires authentication
    """
    try:
        success = service.delete(role_id)
        if success:
            return {"message": "Role deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to delete role")
    except ServiceError as e:
        if e.code == "not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.patch("/{role_id}/soft-delete")
async def soft_delete_role(
    role_id: UUID = Path(..., description="Role ID"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Soft delete a role (mark as deleted without removing from database)
    Requires authentication
    """
    try:
        success = service.soft_delete(role_id, current_user_id=current_user.id)
        if success:
            return {"message": "Role soft deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to soft delete role")
    except ServiceError as e:
        if e.code == "not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        elif e.code == "not_supported":
            raise HTTPException(status_code=400, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.patch("/{role_id}/restore", response_model=DTORoleRetrieve)
async def restore_role(
    role_id: UUID = Path(..., description="Role ID"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Restore a soft-deleted role
    Requires authentication
    """
    try:
        return service.restore(role_id, current_user_id=current_user.id)
    except ServiceError as e:
        if e.code == "not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        elif e.code == "invalid_operation":
            raise HTTPException(status_code=400, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


# Role-specific endpoints
@role.patch("/{role_id}/permissions", response_model=DTORoleRetrieve)
async def update_role_permissions(
    role_id: UUID = Path(..., description="Role ID"),
    permission_data: PermissionUpdateRequest = Body(...),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Update role permissions
    Requires authentication
    """
    try:
        return service.update_permissions(
            role_id=role_id,
            permission_ids=permission_data.permission_ids,
            current_user_id=current_user.id,
        )
    except ServiceError as e:
        if e.code == "not_found" or e.code == "permissions_not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.get("/{role_id}/permissions", response_model=list[dict[str, Any]])
async def get_role_permissions(
    role_id: UUID = Path(..., description="Role ID"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Get all permissions associated with a role
    Requires authentication
    """
    try:
        role = service.get(role_id)
        # Assuming the role DTO includes permissions information
        # If not, you might need to add a method to the service to get role with permissions
        if hasattr(role, "permissions"):
            return role.permissions
        else:
            # If permissions are not included in the DTO, you might need to query them separately
            # This would require additional service method or direct database query
            return []
    except ServiceError as e:
        if e.code == "not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


@role.delete("/{role_id}/permissions")
async def remove_all_role_permissions(
    role_id: UUID = Path(..., description="Role ID"),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Remove all permissions from a role
    Requires authentication
    """
    try:
        service.update_permissions(
            role_id=role_id, permission_ids=[], current_user_id=current_user.id
        )
        return {"message": "All permissions removed from role successfully"}
    except ServiceError as e:
        if e.code == "not_found":
            raise HTTPException(status_code=404, detail=e.message) from e
        raise HTTPException(status_code=400, detail=e.message) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


# Batch operations
@role.patch("/batch/permissions")
async def batch_update_role_permissions(
    updates: list[dict[str, Any]] = Body(
        ..., description="List of role_id and permission_ids pairs"
    ),
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Batch update permissions for multiple roles
    Expected format: [{"role_id": "uuid", "permission_ids": ["uuid1", "uuid2"]}]
    Requires authentication
    """
    try:
        results = []
        errors = []

        for update in updates:
            try:
                role_id = UUID(update["role_id"])
                permission_ids = [UUID(pid) for pid in update["permission_ids"]]

                service.update_permissions(
                    role_id=role_id, permission_ids=permission_ids, current_user_id=current_user.id
                )
                results.append({"role_id": str(role_id), "status": "success"})
            except Exception as e:
                errors.append({"role_id": update.get("role_id"), "error": str(e)})

        return {
            "message": (
                "Batch operation completed. {len(results)} successful, {len(errors)} failed"
            ),
            "results": results,
            "errors": errors,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


# Statistics and reporting endpoints
@role.get("/stats/summary")
async def get_roles_statistics(
    current_user: DTOUserRetrieve = Depends(get_current_user),
    service: ServiceRole = Depends(get_role_service),
):
    """
    Get roles statistics summary
    Requires authentication
    """
    try:
        # Get all roles without pagination to calculate statistics
        all_roles = service.list(page=1, limit=1000, include_deleted=True)
        active_roles = service.list(page=1, limit=1000, include_deleted=False)
        default_roles = service.get_default_roles(include_deleted=False)

        return {
            "total_roles": all_roles["pagination"].total,
            "active_roles": active_roles["pagination"].total,
            "deleted_roles": all_roles["pagination"].total - active_roles["pagination"].total,
            "default_roles": len(default_roles),
            "custom_roles": active_roles["pagination"].total - len(default_roles),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error") from e


# Health check endpoint
@role.get("/health/check")
async def health_check(service: ServiceRole = Depends(get_role_service)):
    """
    Health check endpoint to verify service connectivity
    """
    try:
        # Try to perform a simple query to check database connectivity
        service.list(page=1, limit=1)
        return {"status": "healthy", "service": "role"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service unavailable") from e
