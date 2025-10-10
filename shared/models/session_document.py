from sqlalchemy import Column, ForeignKey, Index, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class SessionDocument(BaseModel):
    """Session document model for tracking generated documents."""

    __tablename__ = "session_documents"
    __table_args__ = (
        Index("idx_session_documents_session_id", "session_id"),
        Index("idx_session_documents_tool_execution_id", "tool_execution_id"),
        Index("idx_session_documents_document_type", "document_type"),
        Index("idx_session_documents_status", "status"),
        Index("idx_session_documents_created_at", "created_at"),
        Index("idx_session_documents_session_created", "session_id", "created_at"),
    )

    # Foreign keys
    session_id = Column(
        String,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    tool_execution_id = Column(
        String,
        ForeignKey("tool_executions.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Document details
    document_type = Column(
        String,
        nullable=False,
    )  # premium_pdf, termination_letter (premium_email is not tracked as a document)
    document_url = Column(String, nullable=True)
    recipient_email = Column(String, nullable=True)  # For emails
    status = Column(String, nullable=False)  # generated, sent, failed
    error_message = Column(String, nullable=True)

    # Relationships
    session = relationship("ChatSession", back_populates="documents")
    tool_execution = relationship("ToolExecution", back_populates="documents")
