"""Document models."""

from sqlalchemy import JSON, Boolean, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from shared.models.base import BaseModel


class Document(BaseModel):
    """Generated document."""

    __tablename__ = "documents"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
        index=True,
    )
    template_id = Column(
        UUID(as_uuid=True),
        ForeignKey("document_templates.id"),
        nullable=True,
    )
    document_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    storage_url = Column(String, nullable=True)
    meta_data = Column(
        JSON,
        default=dict,
    )  # Renamed from 'metadata' (reserved by SQLAlchemy)
    status = Column(String, default="draft")


class DocumentTemplate(BaseModel):
    """Document template."""

    __tablename__ = "document_templates"

    name = Column(String, nullable=False, unique=True)
    template_type = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    variables = Column(JSON, default=list)
    is_active = Column(Boolean, default=True)


class Signature(BaseModel):
    """E-signature record."""

    __tablename__ = "signatures"

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id"),
        nullable=False,
        index=True,
    )
    signer_email = Column(String, nullable=False)
    signer_name = Column(String, nullable=False)
    signature_data = Column(JSON, nullable=False)
    ip_address = Column(String, nullable=True)
    status = Column(String, default="pending")
