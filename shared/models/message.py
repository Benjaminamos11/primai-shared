"""Message model."""

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from shared.models.base import BaseModel


class Message(BaseModel):
    """Individual message in a conversation."""

    __tablename__ = "messages"

    conversation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    sequence = Column(Integer, nullable=False)
    meta_data = Column(
        JSON,
        default=dict,
    )  # Renamed from 'metadata' (reserved by SQLAlchemy)
