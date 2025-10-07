from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.chat_session import ChatSession
from shared.repositories.base_repository import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):
    """Repository for chat session operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(ChatSession, db)

    async def get_by_lead_id(self, lead_id: str) -> Optional[ChatSession]:
        """Get chat session by lead ID."""
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.lead_id == lead_id),
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> List[ChatSession]:
        """Get chat sessions by email."""
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.email == email),
        )
        return list(result.scalars().all())

    async def get_recent_sessions(self, limit: int = 10) -> List[ChatSession]:
        """Get recent chat sessions."""
        result = await self.db.execute(
            select(ChatSession).order_by(ChatSession.created_at.desc()).limit(limit),
        )
        return list(result.scalars().all())
