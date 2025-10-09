from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from shared.models.base import BaseModel


class EmailLog(BaseModel):
    """Email log model."""

    __tablename__ = "email_logs"

    to_email = Column(String, nullable=False)
    cc_email = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    html_size = Column(Integer, nullable=True)
    provider_id = Column(String, nullable=True)
    template = Column(String, nullable=True)
    payload = Column(JSON, nullable=True)
    status = Column(String, nullable=True)
    error = Column(String, nullable=True)
    lead_id = Column(
        String,
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Relationships
    lead = relationship("Lead", back_populates="email_logs")
