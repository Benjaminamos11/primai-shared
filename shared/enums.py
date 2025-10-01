"""Enums for PrimAI shared models."""

from enum import Enum


class EventType(str, Enum):
    """Event types for analytics tracking."""

    CHAT_OPENED = "chat_opened"
    INTENT_DETECTED = "intent_detected"
    PREMIUMS_REQUESTED = "premiums_requested"
    PREMIUMS_RETURNED = "premiums_returned"
    LEAD_UPSERTED = "lead_upserted"
    PDF_GENERATED = "pdf_generated"
    EMAIL_SENT = "email_sent"
    CAL_BOOKED = "cal_booked"
    SESSION_CREATED = "session_created"
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"


class LeadStatus(str, Enum):
    """Lead status."""

    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    CONVERTED = "converted"
    LOST = "lost"


class AppointmentStatus(str, Enum):
    """Appointment status."""

    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class DocumentType(str, Enum):
    """Document types."""

    PREMIUM_COMPARISON = "premium_comparison"
    CANCELLATION_LETTER = "cancellation_letter"
    CHANGE_REQUEST = "change_request"


class EmailStatus(str, Enum):
    """Email delivery status."""

    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    BOUNCED = "bounced"
    ERROR = "error"
