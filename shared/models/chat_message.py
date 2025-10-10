from sqlalchemy import JSON, Column, ForeignKey, Index, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class ChatMessage(BaseModel):
    """Chat message model."""

    __tablename__ = "chat_messages"
    __table_args__ = (
        Index("idx_chat_messages_session_id", "session_id"),
        Index("idx_chat_messages_updated_at", "updated_at"),
    )

    session_id = Column(
        String,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(String, nullable=False)
    meta = Column(JSON, nullable=True)  # Additional metadata

    # Relationships
    session = relationship("ChatSession", back_populates="messages")
    tool_executions = relationship(
        "ToolExecution",
        back_populates="message",
        cascade="all, delete-orphan",
    )
