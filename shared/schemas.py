"""Pydantic schemas for data validation Shared between API and Workers."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field


# Session Schemas
class SessionCreate(BaseModel):
    """Schema for creating a session."""

    session_id: str
    user_data: Dict[str, Any] = {}
    meta_data: Dict[str, Any] = {}  # Renamed from 'metadata' (reserved by SQLAlchemy)


# Conversation Schemas
class ConversationCreate(BaseModel):
    """Schema for creating a conversation."""

    session_id: str
    title: Optional[str] = None
    context: Dict[str, Any] = {}
    meta_data: Dict[str, Any] = {}  # Renamed from 'metadata' (reserved by SQLAlchemy)


# Message Schemas
class MessageCreate(BaseModel):
    """Schema for creating a message."""

    conversation_id: str
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str
    sequence: int
    meta_data: Dict[str, Any] = {}  # Renamed from 'metadata' (reserved by SQLAlchemy)


# Insurance Schemas
class PremiumQueryCreate(BaseModel):
    """Schema for creating a premium query."""

    session_id: str
    insurance_type: str
    query_data: Dict[str, Any]


class QuoteCreate(BaseModel):
    """Schema for creating a quote."""

    premium_query_id: str
    insurer_id: Optional[str] = None
    product_name: str
    annual_premium: float = Field(..., gt=0)
    coverage_details: Dict[str, Any] = {}
    quote_data: Dict[str, Any] = {}


# Document Schemas
class DocumentCreate(BaseModel):
    """Schema for creating a document."""

    session_id: str
    template_id: Optional[str] = None
    document_type: str
    title: str
    content: str
    meta_data: Dict[str, Any] = {}  # Renamed from 'metadata' (reserved by SQLAlchemy)


# Email Schemas
class EmailCreate(BaseModel):
    """Schema for creating an email."""

    session_id: Optional[str] = None
    to_email: EmailStr
    from_email: EmailStr
    subject: str
    body_html: str
    body_text: Optional[str] = None
    meta_data: Dict[str, Any] = {}  # Renamed from 'metadata' (reserved by SQLAlchemy)


# Lead Schemas
class LeadCreate(BaseModel):
    """Schema for creating a lead."""

    session_id: Optional[str] = None
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    lead_source: Optional[str] = None
    lead_data: Dict[str, Any] = {}


# Appointment Schemas
class AppointmentCreate(BaseModel):
    """Schema for creating an appointment."""

    lead_id: str
    scheduled_at: datetime
    duration_minutes: int = 30
    meeting_type: str
    meeting_url: Optional[str] = None
    notes: Dict[str, Any] = {}
