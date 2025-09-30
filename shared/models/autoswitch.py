"""Autoswitch models"""
from sqlalchemy import Column, String, Text, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from shared.models.base import BaseModel


class AutoswitchProfile(BaseModel):
    """Autoswitch user profile"""
    
    __tablename__ = "autoswitch_profiles"
    
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"), nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    current_policy_data = Column(JSON, default=dict)
    preferences = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)


class AutoswitchRun(BaseModel):
    """Autoswitch comparison run"""
    
    __tablename__ = "autoswitch_runs"
    
    profile_id = Column(UUID(as_uuid=True), ForeignKey("autoswitch_profiles.id"), nullable=False, index=True)
    run_type = Column(String, nullable=False)  # manual, scheduled
    results = Column(JSON, default=dict)
    savings_potential = Column(String, nullable=True)
    status = Column(String, default="pending")
    completed_at = Column(DateTime, nullable=True)


class AutoswitchTask(BaseModel):
    """Individual task in autoswitch process"""
    
    __tablename__ = "autoswitch_tasks"
    
    run_id = Column(UUID(as_uuid=True), ForeignKey("autoswitch_runs.id"), nullable=False, index=True)
    task_type = Column(String, nullable=False)
    task_data = Column(JSON, default=dict)
    result = Column(Text, nullable=True)
    status = Column(String, default="pending")
    error_message = Column(Text, nullable=True)
