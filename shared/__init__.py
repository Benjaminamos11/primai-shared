"""PrimAI Shared Library Shared Pydantic schemas, SQLAlchemy models, and
utilities for API and Workers."""

from shared.constants import (  # noqa: I004
    DOCUMENT_STATUS,
    EMAIL_STATUS,
    INSURANCE_TYPES,
    LEAD_STATUS,
    QUOTE_STATUS,
)
from shared.database import AsyncSessionLocal, engine, get_db  # noqa: I004
from shared.models import (  # noqa: I004
    Appointment,
    AutoswitchProfile,
    AutoswitchRun,
    AutoswitchTask,
    Base,
    Conversation,
    Document,
    DocumentTemplate,
    Email,
    EmailEvent,
    Event,
    Insurer,
    InsurerContact,
    Lead,
    LLMRun,
    Message,
    PremiumQuery,
    Quote,
    Session,
    Signature,
)
from shared.schemas import (  # noqa: I004
    ConversationCreate,
    DocumentCreate,
    EmailCreate,
    LeadCreate,
    MessageCreate,
    PremiumQueryCreate,
    QuoteCreate,
    SessionCreate,
)
from shared.utils import (  # noqa: I004
    format_currency_chf,
    format_swiss_phone,
    validate_email,
    validate_swiss_phone,
    validate_swiss_postal_code,
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
