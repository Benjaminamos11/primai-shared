from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.lead import Lead
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

    async def get_by_session_id(self, session_id: str) -> Optional[Lead]:
        """Get lead by session ID."""
        result = await self.db.execute(
            select(Lead).where(Lead.session_id == session_id),
        )
        return result.scalar_one_or_none()

    async def get_recent_leads(self, limit: int = 10) -> List[Lead]:
        """Get recent leads."""
        result = await self.db.execute(
            select(Lead).order_by(Lead.created_at.desc()).limit(limit),
        )
        return list(result.scalars().all())

    async def get_consented_leads(self) -> List[Lead]:
        """Get leads who have given consent."""
        result = await self.db.execute(
            select(Lead).where(Lead.consent == True),  # noqa: E712
        )
        return list(result.scalars().all())
