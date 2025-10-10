from sqlalchemy import JSON, Boolean, Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class ChatSession(BaseModel):
    """Chat session model."""

    __tablename__ = "chat_sessions"
    __table_args__ = (
        Index("idx_chat_sessions_plz", "plz"),
        Index("idx_chat_sessions_email", "email"),
        Index("idx_chat_sessions_updated_at", "updated_at"),
    )

    # Session info
    source = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    ip_hash = Column(String, nullable=True)
    locale = Column(String, nullable=True)

    # User data
    plz = Column(String, nullable=True)  # Postal code
    canton = Column(String, nullable=True)
    yob = Column(Integer, nullable=True)  # Year of birth
    age = Column(Integer, nullable=True)
    model_pref = Column(String, nullable=True)  # Car model preference
    deductible = Column(Integer, nullable=True)
    accident = Column(Boolean, nullable=True)
    household_json = Column(JSON, nullable=True)
    email = Column(String, nullable=True)
    consent = Column(Boolean, default=False)
    lead_id = Column(
        String,
        ForeignKey(
            "leads.id",
            ondelete="SET NULL",
            use_alter=True,
            name="fk_chat_sessions_lead_id",
        ),
        nullable=True,
        unique=True,
    )

    # Relationships
    lead = relationship(
        "Lead",
        foreign_keys="[ChatSession.lead_id]",
        uselist=False,
    )
    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    funnel_events = relationship("FunnelEvent", back_populates="session")
    tool_executions = relationship(
        "ToolExecution",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    documents = relationship(
        "SessionDocument",
        back_populates="session",
        cascade="all, delete-orphan",
    )
