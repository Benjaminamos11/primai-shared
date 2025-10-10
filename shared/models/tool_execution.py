from sqlalchemy import JSON, Column, ForeignKey, Index, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class ToolExecution(BaseModel):
    """Tool execution model for tracking AI tool calls."""

    __tablename__ = "tool_executions"
    __table_args__ = (
        Index("idx_tool_executions_session_id", "session_id"),
        Index("idx_tool_executions_message_id", "message_id"),
        Index("idx_tool_executions_tool_name", "tool_name"),
        Index("idx_tool_executions_created_at", "created_at"),
        Index("idx_tool_executions_session_created", "session_id", "created_at"),
    )

    # Foreign keys
    session_id = Column(
        String,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    message_id = Column(
        String,
        ForeignKey("chat_messages.id", ondelete="CASCADE"),
        nullable=True,
    )

    # Tool details
    tool_name = Column(String, nullable=False)
    tool_arguments = Column(JSON, nullable=True)  # Input arguments
    tool_result = Column(JSON, nullable=True)  # Output result
    status = Column(String, nullable=False)  # success, error

    # Relationships
    session = relationship("ChatSession", back_populates="tool_executions")
    message = relationship("ChatMessage", back_populates="tool_executions")
    documents = relationship(
        "SessionDocument",
        back_populates="tool_execution",
        cascade="all, delete-orphan",
    )
