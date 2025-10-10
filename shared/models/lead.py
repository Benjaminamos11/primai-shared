from sqlalchemy import Boolean, Column, ForeignKey, Index, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class Lead(BaseModel):
    """Lead model."""

    __tablename__ = "leads"
    __table_args__ = (
        Index("idx_leads_email", "email"),
        Index("idx_leads_first_name", "first_name"),
        Index("idx_leads_last_name", "last_name"),
        Index("idx_leads_phone", "phone"),
        Index("idx_leads_updated_at", "updated_at"),
    )

    # Basic info
    email = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    locale = Column(String, nullable=True)
    consent = Column(Boolean, default=False)
    source = Column(String, nullable=True)
    session_id = Column(
        String,
        ForeignKey("chat_sessions.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )
    summary_html = Column(String, nullable=True)
    summary_text = Column(String, nullable=True)
    annual_switch = Column(Boolean, default=False)

    # Relationships
    session = relationship(
        "ChatSession",
        foreign_keys="[Lead.session_id]",
        uselist=False,
        viewonly=True,
    )
    email_logs = relationship("EmailLog", back_populates="lead")
    funnel_events = relationship("FunnelEvent", back_populates="lead")
