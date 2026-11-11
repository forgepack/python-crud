from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import MixinAudit, MixinSoftDelete
from app.models.join import user_roles

if TYPE_CHECKING:
    from app.models.role import Role


class User(Base, MixinAudit, MixinSoftDelete):
    """User Model"""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    _password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True, doc="Whether user account is active"
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, doc="Whether user email is verified"
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, doc="Last successful login timestamp"
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, doc="Count of consecutive failed login attempts"
    )
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, doc="Account lock expiration timestamp"
    )

    # relationships
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
        order_by="Role.name",
        doc="Roles assigned to the user",
    )

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"
