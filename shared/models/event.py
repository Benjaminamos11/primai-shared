"""Event and LLM run tracking models."""

from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID

from shared.models.base import BaseModel


class Event(BaseModel):
    """Analytics event."""

    __tablename__ = "events"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=True,
        index=True,
    )
    event_type = Column(String, nullable=False, index=True)
    event_data = Column(JSON, default=dict)
    user_agent = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)


class LLMRun(BaseModel):
    """LLM API call tracking."""

    __tablename__ = "llm_runs"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=True,
        index=True,
    )
    message_id = Column(
        UUID(as_uuid=True),
        ForeignKey("messages.id"),
        nullable=True,
        index=True,
    )
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    tokens_input = Column(Integer, default=0)
    tokens_output = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    latency_ms = Column(Integer, nullable=True)
    meta_data = Column(
        JSON,
        default=dict,
    )  # Renamed from 'metadata' (reserved by SQLAlchemy)
    status = Column(String, default="pending")
