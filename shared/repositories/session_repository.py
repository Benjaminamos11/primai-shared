"""Session repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models import Session
from shared.repositories.base_repository import BaseRepository


class SessionRepository(BaseRepository[Session]):
    """Repository for session operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Session, db)

    async def get_by_session_id(self, session_id: str) -> Optional[Session]:
        """Get session by session_id string."""
        result = await self.db.execute(
            select(Session).where(Session.session_id == session_id),
        )
        return result.scalar_one_or_none()

    async def get_or_create(self, session_id: str, **kwargs) -> Session:
        """Get existing session or create new one."""
        session = await self.get_by_session_id(session_id)
        if session:
            return session

        return await self.create(session_id=session_id, **kwargs)
