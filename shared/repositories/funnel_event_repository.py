from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.funnel_event import FunnelEvent
from shared.repositories.base_repository import BaseRepository


class FunnelEventRepository(BaseRepository[FunnelEvent]):
    """Repository for funnel event operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(FunnelEvent, db)

    async def get_by_session_id(self, session_id: str) -> List[FunnelEvent]:
        """Get all events for a session."""
        result = await self.db.execute(
            select(FunnelEvent)
            .where(FunnelEvent.session_id == session_id)
            .order_by(FunnelEvent.created_at),
        )
        return list(result.scalars().all())

    async def get_by_event_type(
        self,
        event_type: str,
        limit: int = 100,
    ) -> List[FunnelEvent]:
        """Get events by type."""
        result = await self.db.execute(
            select(FunnelEvent)
            .where(FunnelEvent.event_type == event_type)
            .order_by(FunnelEvent.created_at.desc())
            .limit(limit),
        )
        return list(result.scalars().all())

    async def get_by_lead_id(self, lead_id: str) -> List[FunnelEvent]:
        """Get all events for a lead."""
        result = await self.db.execute(
            select(FunnelEvent)
            .where(FunnelEvent.lead_id == lead_id)
            .order_by(FunnelEvent.created_at),
        )
        return list(result.scalars().all())

    async def get_recent_events(self, limit: int = 100) -> List[FunnelEvent]:
        """Get recent funnel events."""
        result = await self.db.execute(
            select(FunnelEvent).order_by(FunnelEvent.created_at.desc()).limit(limit),
        )
        return list(result.scalars().all())
