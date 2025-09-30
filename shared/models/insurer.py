"""Insurer models."""

from sqlalchemy import JSON, Boolean, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from shared.models.base import BaseModel


class Insurer(BaseModel):
    """Insurance company."""

    __tablename__ = "insurers"

    name = Column(String, nullable=False, unique=True)
    short_name = Column(String, nullable=True)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    api_config = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)


class InsurerContact(BaseModel):
    """Insurer contact person."""

    __tablename__ = "insurer_contacts"

    insurer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("insurers.id"),
        nullable=False,
        index=True,
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
