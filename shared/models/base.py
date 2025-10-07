from typing import Any
from uuid import uuid4

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """Base model with common fields."""

    __abstract__ = True

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
