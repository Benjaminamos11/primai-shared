from sqlalchemy import JSON, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class ChatSession(BaseModel):
    """Chat session model."""

    __tablename__ = "chat_sessions"

    # Session info
    source = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    ip_hash = Column(String, nullable=True)
    locale = Column(String, nullable=True)

    # User data
    plz = Column(String, nullable=True, index=True)  # Postal code
    canton = Column(String, nullable=True)
    yob = Column(Integer, nullable=True)  # Year of birth
    age = Column(Integer, nullable=True)
    model_pref = Column(String, nullable=True)  # Car model preference
    deductible = Column(Integer, nullable=True)
    accident = Column(Boolean, nullable=True)
    household_json = Column(JSON, nullable=True)
    email = Column(String, nullable=True, index=True)
    consent = Column(Boolean, default=False)
    lead_id = Column(String, nullable=True, unique=True, index=True)

    # Relationships
    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
    )
