"""User model for authentication and authorization."""

from sqlalchemy import Boolean, Column, DateTime, Index, String

from shared.models.base import BaseModel


class User(BaseModel):
    """User model for authentication."""

    __tablename__ = "users"

    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="admin")
    is_active = Column(Boolean, default=True)

    # Track when the user was last active (login/refresh)
    last_active = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"

    __table_args__ = (
        # Commonly queried columns
        Index("ix_users_is_active_updated_at", "is_active", "updated_at"),
        Index("ix_users_role_is_active", "role", "is_active"),
    )
