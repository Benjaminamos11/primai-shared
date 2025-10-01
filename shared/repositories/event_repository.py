"""Event repository."""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.enums import EventType
from shared.models import Event
from shared.repositories.base_repository import BaseRepository


class EventRepository(BaseRepository[Event]):
    """Repository for event tracking operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Event, db)

    async def get_by_session(
        self,
        session_id: UUID,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Event]:
        """Get all events for a session."""
        result = await self.db.execute(
            select(Event)
            .where(Event.session_id == session_id)
            .order_by(Event.created_at)
            .offset(skip)
            .limit(limit),
        )
        return list(result.scalars().all())

    async def track(
        self,
        event_type: EventType,
        session_id: Optional[UUID] = None,
        event_data: Optional[dict] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> Event:
        """Track a new event."""
        return await self.create(
            event_type=event_type.value,
            session_id=session_id,
            event_data=event_data or {},
            user_agent=user_agent,
            ip_address=ip_address,
        )
