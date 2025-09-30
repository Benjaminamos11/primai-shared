"""Lead and appointment models"""
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from shared.models.base import BaseModel


class Lead(BaseModel):
    """Lead/prospect"""
    
    __tablename__ = "leads"
    
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=True, index=True)
    email = Column(String, nullable=False, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    lead_source = Column(String, nullable=True)
    lead_data = Column(JSON, default=dict)
    status = Column(String, default="new")


class Appointment(BaseModel):
    """Scheduled appointment"""
    
    __tablename__ = "appointments"
    
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"), nullable=False, index=True)
    scheduled_at = Column(DateTime, nullable=False)
    duration_minutes = Column(String, default="30")
    meeting_type = Column(String, nullable=False)
    meeting_url = Column(String, nullable=True)
    notes = Column(JSON, default=dict)
    status = Column(String, default="scheduled")
