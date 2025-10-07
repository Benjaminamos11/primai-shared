from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.chat_message import ChatMessage
from shared.repositories.base_repository import BaseRepository


class ChatMessageRepository(BaseRepository[ChatMessage]):
    """Repository for chat message operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(ChatMessage, db)

    async def get_by_session_id(self, session_id: str) -> List[ChatMessage]:
        """Get all messages for a session."""
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at),
        )
        return list(result.scalars().all())

    async def get_latest_message(self, session_id: str) -> ChatMessage:
        """Get the latest message for a session."""
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(1),
        )
        return result.scalar_one_or_none()
