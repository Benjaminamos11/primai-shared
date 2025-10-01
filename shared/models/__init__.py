"""SQLAlchemy Models Shared between API and Workers for database access."""

from shared.models.autoswitch import AutoswitchProfile, AutoswitchRun, AutoswitchTask
from shared.models.base import Base
from shared.models.conversation import Conversation
from shared.models.document import Document, DocumentTemplate, Signature
from shared.models.email import Email, EmailEvent
from shared.models.event import Event, LLMRun
from shared.models.insurer import Insurer, InsurerContact
from shared.models.lead import Appointment, Lead
from shared.models.message import Message
from shared.models.premium_query import PremiumQuery, Quote
from shared.models.session import Session

__all__ = [
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
]
