from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.tool_execution import ToolExecution
from shared.repositories.base_repository import BaseRepository


class ToolExecutionRepository(BaseRepository[ToolExecution]):
    """Repository for tool execution operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(ToolExecution, db)

    async def get_by_session_id(self, session_id: str) -> List[ToolExecution]:
        """Get all tool executions for a session."""
        result = await self.db.execute(
            select(ToolExecution)
            .where(ToolExecution.session_id == session_id)
            .order_by(ToolExecution.created_at),
        )
        return list(result.scalars().all())

    async def get_by_message_id(self, message_id: str) -> List[ToolExecution]:
        """Get all tool executions for a message."""
        result = await self.db.execute(
            select(ToolExecution)
            .where(ToolExecution.message_id == message_id)
            .order_by(ToolExecution.created_at),
        )
        return list(result.scalars().all())

    async def get_by_tool_name(
        self,
        session_id: str,
        tool_name: str,
    ) -> List[ToolExecution]:
        """Get all executions of a specific tool for a session."""
        result = await self.db.execute(
            select(ToolExecution)
            .where(
                ToolExecution.session_id == session_id,
                ToolExecution.tool_name == tool_name,
            )
            .order_by(ToolExecution.created_at),
        )
        return list(result.scalars().all())

    async def get_tool_executions_by_session_paginated(
        self,
        session_id: str,
        page: int = 1,
        limit: int = 10,
    ) -> Tuple[List[ToolExecution], int]:
        """Get paginated tool executions for a session with only specific
        fields.

        Args:
            session_id: Session ID to get tool executions for
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (tool executions list, total count)
        """
        # Build query with selected fields only
        query = select(
            ToolExecution.id,
            ToolExecution.tool_name,
            ToolExecution.tool_arguments,
            ToolExecution.tool_result,
            ToolExecution.status,
            ToolExecution.created_at,
        ).where(ToolExecution.session_id == session_id)

        # Get total count
        count_query = (
            select(func.count())
            .select_from(ToolExecution)
            .where(ToolExecution.session_id == session_id)
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination and sorting by created_at desc
        skip = (page - 1) * limit
        query = query.order_by(ToolExecution.created_at.asc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        tool_executions = [ToolExecution(**dict(row._mapping)) for row in result]

        return tool_executions, total
