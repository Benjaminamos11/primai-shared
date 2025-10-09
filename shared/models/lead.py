from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class Lead(BaseModel):
    """Lead model."""

    __tablename__ = "leads"

    # Basic info
    email = Column(String, nullable=False, index=True)
    first_name = Column(String, nullable=True, index=True)
    last_name = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True, index=True)
    locale = Column(String, nullable=True)
    consent = Column(Boolean, default=False)
    source = Column(String, nullable=True)
    session_id = Column(String, nullable=True, unique=True)
    summary_html = Column(String, nullable=True)
    summary_text = Column(String, nullable=True)
    annual_switch = Column(Boolean, default=False)

    # Relationships
    email_logs = relationship("EmailLog", back_populates="lead")
