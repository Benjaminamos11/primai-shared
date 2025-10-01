"""Lead repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Lead
from shared.repositories.base_repository import BaseRepository


class LeadRepository(BaseRepository[Lead]):
    """Repository for lead operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Lead, db)

    async def get_by_email(self, email: str) -> Optional[Lead]:
        """Get lead by email."""
        result = await self.db.execute(
            select(Lead).where(Lead.email == email),
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        email: str,
        session_id: Optional[str] = None,
        **kwargs,
    ) -> Lead:
        """Create or update lead by email."""
        lead = await self.get_by_email(email)

        if lead:
            # Update existing
            for key, value in kwargs.items():
                if value is not None:
                    setattr(lead, key, value)
            await self.db.commit()
            await self.db.refresh(lead)
            return lead

        # Create new
        return await self.create(
            email=email,
            session_id=session_id,
            **kwargs,
        )
