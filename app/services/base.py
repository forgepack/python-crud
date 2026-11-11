import logging
from datetime import datetime
from math import ceil
from typing import Any, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError as SAIntegrityError
from sqlalchemy.orm import Session

from app.database import Base
from app.schemas.base import DTOPagination

TModel = TypeVar("TModel", bound=Base)
TCreateSchema = TypeVar("TCreateSchema", bound=BaseModel)
TUpdateSchema = TypeVar("TUpdateSchema", bound=BaseModel)
TResponseSchema = TypeVar("TResponseSchema", bound=BaseModel)

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    """Generic error in the service layer"""

    def __init__(self, message: str, code: str = "service_error"):
        self.message = message
        self.code = code
        super().__init__(message)


class ServiceBase[
    TModel: Base,
    TCreateSchema: BaseModel,
    TUpdateSchema: BaseModel,
    TResponseSchema: BaseModel,
]:
    """Generic service for CRUD operations"""

    def __init__(self, model: type[TModel], db: Session, response_schema: type[TResponseSchema]):
        self.model = model
        self.db = db
        self.response_schema = response_schema

    def _get_instance(self, id: UUID) -> TModel | None:
        """Fetches a resource without throwing an error"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def _apply_audit_fields(self, instance: TModel, current_user_id: UUID | None = None) -> TModel:
        """Fills in audit fields"""
        if hasattr(instance, "created_by") and not instance.created_by:
            instance.created_by = current_user_id
        if hasattr(instance, "updated_by"):
            instance.updated_by = current_user_id
        return instance

    def _to_response_dto(self, instance: TModel) -> TResponseSchema:
        """Convert entity to DTO"""
        return self.response_schema.model_validate(instance, from_attributes=True)

    def _handle_exception(self, e: Exception, action: str):
        """Standardizes rollback and log"""
        self.db.rollback()
        logger.error(f"Erro ao {action} {self.model.__name__}: {str(e)}")
        if isinstance(e, SAIntegrityError):
            raise ServiceError(
                f"Integrity error when {action} {self.model.__name__}", code="integrity_error"
            )
        raise ServiceError(f"Unexpected error when {action} {self.model.__name__}")

    def get(self, id: UUID, include_deleted: bool = False) -> TResponseSchema:
        """Get a single resource by ID"""
        query = self.db.query(self.model).filter(self.model.id == id)
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        instance = query.first()
        if not instance:
            raise ServiceError(f"{self.model.__name__} with id {id} not found", code="not_found")
        return self._to_response_dto(instance)

    def list(
        self, page: int = 1, limit: int = 20, include_deleted: bool = False, **filters: Any
    ) -> dict[str, Any]:
        """List with optional filters and pagination"""
        query = self.db.query(self.model)
        model_columns = set(c.key for c in inspect(self.model).mapper.column_attrs)
        for attr, value in filters.items():
            if attr in model_columns:
                query = query.filter(getattr(self.model, attr) == value)
        if not include_deleted and hasattr(self.model, "deleted_at"):
            query = query.filter(self.model.deleted_at.is_(None))
        total = query.count()
        items = query.offset((page - 1) * limit).limit(limit).all()
        total_pages = ceil(total / limit) if limit else 1
        return {
            "items": [self._to_response_dto(item) for item in items],
            "pagination": DTOPagination(
                total=total,
                page=page,
                limit=limit,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1,
            ),
        }

    def create(
        self, create_dto: TCreateSchema, current_user_id: UUID | None = None
    ) -> TResponseSchema:
        """Create a new resource"""
        try:
            instance = self.model(**create_dto.model_dump(exclude_unset=True))
            self._apply_audit_fields(instance, current_user_id)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return self._to_response_dto(instance)
        except Exception as e:
            self._handle_exception(e, "create")

    def update(
        self, id: UUID, update_dto: TUpdateSchema, current_user_id: UUID | None = None
    ) -> TResponseSchema:
        """Update an existing resource"""
        instance = self._get_instance(id)
        if not instance:
            raise ServiceError(f"{self.model.__name__} with id {id} not found", code="not_found")
        try:
            update_data = update_dto.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(instance, field, value)
            if hasattr(instance, "updated_by"):
                instance.updated_by = current_user_id
            self.db.commit()
            self.db.refresh(instance)
            return self._to_response_dto(instance)
        except Exception as e:
            self._handle_exception(e, "update")

    def delete(self, id: UUID) -> bool:
        """Hard delete: permanently remove the record from the bank."""
        instance = self._get_instance(id)
        if not instance:
            raise ServiceError(f"{self.model.__name__} with id {id} not found", code="not_found")
        try:
            self.db.delete(instance)
            self.db.commit()
            return True
        except Exception as e:
            self._handle_exception(e, "excluir")

    def soft_delete(self, id: UUID, current_user_id: UUID | None = None) -> bool:
        """Soft delete: mark as deleted without removing from the database."""
        instance = self._get_instance(id)
        if not instance:
            raise ServiceError(f"{self.model.__name__} with id {id} not found", code="not_found")
        if not hasattr(self.model, "deleted_at"):
            raise ServiceError(
                f"{self.model.__name__} does not support soft delete", code="not_supported"
            )
        try:
            instance.deleted_at = datetime.now()
            if hasattr(instance, "deleted_by"):
                instance.deleted_by = current_user_id
            self.db.commit()
            return True
        except Exception as e:
            self._handle_exception(e, "excluir")

    def restore(self, id: UUID, current_user_id: UUID | None = None) -> TResponseSchema:
        """Restore a soft-deleted resource"""
        if not hasattr(self.model, "deleted_at"):
            raise ServiceError(
                f"{self.model.__name__} does not support restore", code="invalid_operation"
            )
        instance = self._get_instance(id)
        if not instance:
            raise ServiceError(f"{self.model.__name__} with id {id} not found", code="not_found")
        if not instance.deleted_at:
            raise ServiceError(
                f"{self.model.__name__} with id {id} is not deleted", code="invalid_operation"
            )
        try:
            instance.deleted_at = None
            instance.deleted_by = None
            if hasattr(instance, "updated_by"):
                instance.updated_by = current_user_id
            self.db.commit()
            self.db.refresh(instance)
            return self._to_response_dto(instance)
        except Exception as e:
            self._handle_exception(e, "restore")
