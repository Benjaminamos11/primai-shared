from sqlalchemy import JSON, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class ChatMessage(BaseModel):
    """Chat message model."""

    __tablename__ = "chat_messages"

    session_id = Column(
        String,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(String, nullable=False)
    tool_name = Column(String, nullable=True)  # For tool calls
    meta = Column(JSON, nullable=True)  # Additional metadata

    # Relationships
    session = relationship("ChatSession", back_populates="messages")
