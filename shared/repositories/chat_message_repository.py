from typing import List, Tuple

from sqlalchemy import func, select
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

    async def get_messages_by_session_paginated(
        self,
        session_id: str,
        page: int = 1,
        limit: int = 10,
    ) -> Tuple[List[ChatMessage], int]:
        """Get paginated messages for a session.

        Args:
            session_id: Session ID to get messages for
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (messages list, total count)
        """
        # Build query with selected fields only
        query = select(
            ChatMessage.id,
            ChatMessage.session_id,
            ChatMessage.role,
            ChatMessage.content,
            ChatMessage.created_at,
            ChatMessage.updated_at,
        ).where(ChatMessage.session_id == session_id)

        # Get total count
        count_query = (
            select(func.count())
            .select_from(ChatMessage)
            .where(
                ChatMessage.session_id == session_id,
            )
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination and sorting by updated_at desc
        skip = (page - 1) * limit
        query = query.order_by(ChatMessage.updated_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        messages = [ChatMessage(**dict(row._mapping)) for row in result]

        return messages, total
