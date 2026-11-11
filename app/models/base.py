from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import UUID as UUID_
from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models"""

    pass


class MixinAudit:
    """Mixin for audit"""

    id: Mapped[UUID] = mapped_column(UUID_(as_uuid=True), primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[UUID | None] = mapped_column(
        UUID_(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    updated_by: Mapped[UUID | None] = mapped_column(
        UUID_(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    version_id: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False, doc="Optimistic locking version"
    )

    __mapper_args__ = {"version_id_col": version_id, "version_id_generator": True}


class MixinSoftDelete:
    """Mixin for soft delete"""

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[UUID | None] = mapped_column(
        UUID_(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
