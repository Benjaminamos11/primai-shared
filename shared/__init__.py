"""
PrimAI Shared Library
Shared Pydantic schemas, SQLAlchemy models, and utilities for API and Workers
"""

# Pydantic Schemas (for validation)
from shared.schemas import (
    SessionCreate,
    ConversationCreate,
    MessageCreate,
    PremiumQueryCreate,
    QuoteCreate,
    DocumentCreate,
    EmailCreate,
    LeadCreate,
)

# SQLAlchemy Models (for database)
from shared.models import (
    Base,
    Session,
    Conversation,
    Message,
    PremiumQuery,
    Quote,
    Document,
    DocumentTemplate,
    Signature,
    Email,
    EmailEvent,
    Lead,
    Appointment,
    Event,
    LLMRun,
    Insurer,
    InsurerContact,
    AutoswitchProfile,
    AutoswitchRun,
    AutoswitchTask,
)

# Database
from shared.database import engine, AsyncSessionLocal, get_db

# Constants
from shared.constants import (
    INSURANCE_TYPES,
    DOCUMENT_STATUS,
    EMAIL_STATUS,
    LEAD_STATUS,
    QUOTE_STATUS,
)

# Utilities
from shared.utils import (
    validate_email,
    validate_swiss_phone,
    validate_swiss_postal_code,
    format_currency_chf,
    format_swiss_phone,
)

__all__ = [
    # Schemas (Pydantic - for validation)
    "SessionCreate",
    "ConversationCreate",
    "MessageCreate",
    "PremiumQueryCreate",
    "QuoteCreate",
    "DocumentCreate",
    "EmailCreate",
    "LeadCreate",
    # Models (SQLAlchemy - for database)
    "Base",
    "Session",
    "Conversation",
    "Message",
    "PremiumQuery",
    "Quote",
    "Document",
    "DocumentTemplate",
    "Signature",
    "Email",
    "EmailEvent",
    "Lead",
    "Appointment",
    "Event",
    "LLMRun",
    "Insurer",
    "InsurerContact",
    "AutoswitchProfile",
    "AutoswitchRun",
    "AutoswitchTask",
    # Database
    "engine",
    "AsyncSessionLocal",
    "get_db",
    # Constants
    "INSURANCE_TYPES",
    "DOCUMENT_STATUS",
    "EMAIL_STATUS",
    "LEAD_STATUS",
    "QUOTE_STATUS",
    # Utils
    "validate_email",
    "validate_swiss_phone",
    "validate_swiss_postal_code",
    "format_currency_chf",
    "format_swiss_phone",
]
