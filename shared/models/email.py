"""Email models"""
from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from shared.models.base import BaseModel


class Email(BaseModel):
    """Sent email record"""
    
    __tablename__ = "emails"
    
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=True, index=True)
    to_email = Column(String, nullable=False)
    from_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body_html = Column(Text, nullable=False)
    body_text = Column(Text, nullable=True)
    provider_id = Column(String, nullable=True)
    meta_data = Column(JSON, default=dict)  # Renamed from 'metadata' (reserved by SQLAlchemy)
    status = Column(String, default="pending")


class EmailEvent(BaseModel):
    """Email delivery events (webhooks from Resend)"""
    
    __tablename__ = "email_events"
    
    email_id = Column(UUID(as_uuid=True), ForeignKey("emails.id"), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    event_data = Column(JSON, nullable=False)
