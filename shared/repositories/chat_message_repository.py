from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
        """Get paginated messages for a session with tool executions and
        documents.

        Args:
            session_id: Session ID to get messages for
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (messages list, total count)
        """
        # Get total count
        count_query = (
            select(func.count())
            .select_from(ChatMessage)
            .where(ChatMessage.session_id == session_id)
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # Build query with eager loading of tool_executions and their documents
        skip = (page - 1) * limit

        # Import ToolExecution to access its relationships
        from shared.models.tool_execution import ToolExecution

        query = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .options(
                selectinload(ChatMessage.tool_executions).selectinload(
                    ToolExecution.documents,
                ),
            )
            .order_by(ChatMessage.updated_at.asc())
            .offset(skip)
            .limit(limit)
        )

        result = await self.db.execute(query)
        messages = list(result.scalars().all())

        return messages, total
