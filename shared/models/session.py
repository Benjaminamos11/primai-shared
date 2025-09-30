"""Session model."""

from sqlalchemy import JSON, Column, String

from shared.models.base import BaseModel


class Session(BaseModel):
    """User session tracking."""

    __tablename__ = "sessions"

    session_id = Column(String, unique=True, index=True, nullable=False)
    user_data = Column(JSON, default=dict)
    meta_data = Column(
        JSON,
        default=dict,
    )  # Renamed from 'metadata' (reserved by SQLAlchemy)
