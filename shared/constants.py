"""Constants used across API and Workers."""

# Insurance Types
INSURANCE_TYPES = {
    "HEALTH": "health",
    "VEHICLE": "vehicle",
    "HOUSEHOLD": "household",
    "LIABILITY": "liability",
    "LIFE": "life",
    "LEGAL": "legal",
}

INSURANCE_TYPE_LABELS = {
    "health": "Krankenversicherung",
    "vehicle": "Autoversicherung",
    "household": "Hausratversicherung",
    "liability": "Haftpflichtversicherung",
    "life": "Lebensversicherung",
    "legal": "Rechtsschutzversicherung",
}

# Document Status
DOCUMENT_STATUS = {
    "DRAFT": "draft",
    "PENDING_SIGNATURE": "pending_signature",
    "SIGNED": "signed",
    "COMPLETED": "completed",
    "CANCELLED": "cancelled",
}

# Email Status
EMAIL_STATUS = {
    "PENDING": "pending",
    "SENT": "sent",
    "DELIVERED": "delivered",
    "BOUNCED": "bounced",
    "FAILED": "failed",
}

# Lead Status
LEAD_STATUS = {
    "NEW": "new",
    "CONTACTED": "contacted",
    "QUALIFIED": "qualified",
    "CONVERTED": "converted",
    "LOST": "lost",
}

# Quote Status
QUOTE_STATUS = {
    "DRAFT": "draft",
    "ACTIVE": "active",
    "EXPIRED": "expired",
    "ACCEPTED": "accepted",
}

# Message Roles
MESSAGE_ROLES = {
    "USER": "user",
    "ASSISTANT": "assistant",
    "SYSTEM": "system",
}

# LLM Providers
LLM_PROVIDERS = {
    "OPENAI": "openai",
    "ANTHROPIC": "anthropic",
}
