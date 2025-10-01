"""Conversation model."""

from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from shared.models.base import BaseModel


class Conversation(BaseModel):
    """Conversation/thread of messages."""

    __tablename__ = "conversations"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )
    title = Column(String, nullable=True)
    context = Column(JSON, default=dict)
    meta_data = Column(
        JSON,
        default=dict,
    )  # Renamed from 'metadata' (reserved by SQLAlchemy)
