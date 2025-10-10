from typing import List, Tuple

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.session_document import SessionDocument
from shared.repositories.base_repository import BaseRepository


class SessionDocumentRepository(BaseRepository[SessionDocument]):
    """Repository for session document operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(SessionDocument, db)

    async def get_by_session_id(self, session_id: str) -> List[SessionDocument]:
        """Get all documents for a session."""
        result = await self.db.execute(
            select(SessionDocument)
            .where(SessionDocument.session_id == session_id)
            .order_by(SessionDocument.created_at),
        )
        return list(result.scalars().all())

    async def get_by_tool_execution_id(
        self,
        tool_execution_id: str,
    ) -> List[SessionDocument]:
        """Get all documents for a tool execution."""
        result = await self.db.execute(
            select(SessionDocument)
            .where(SessionDocument.tool_execution_id == tool_execution_id)
            .order_by(SessionDocument.created_at),
        )
        return list(result.scalars().all())

    async def get_by_document_type(
        self,
        session_id: str,
        document_type: str,
    ) -> List[SessionDocument]:
        """Get all documents of a specific type for a session."""
        result = await self.db.execute(
            select(SessionDocument)
            .where(
                SessionDocument.session_id == session_id,
                SessionDocument.document_type == document_type,
            )
            .order_by(SessionDocument.created_at),
        )
        return list(result.scalars().all())

    async def get_documents_by_session_paginated(
        self,
        session_id: str,
        page: int = 1,
        limit: int = 10,
    ) -> Tuple[List[SessionDocument], int]:
        """Get paginated documents for a session with only specific fields.

        Args:
            session_id: Session ID to get documents for
            page: Page number (1-indexed)
            limit: Items per page

        Returns:
            Tuple of (documents list, total count)
        """
        # Build query with selected fields only
        query = select(
            SessionDocument.id,
            SessionDocument.document_type,
            SessionDocument.document_url,
            SessionDocument.recipient_email,
            SessionDocument.status,
            SessionDocument.error_message,
            SessionDocument.created_at,
        ).where(SessionDocument.session_id == session_id)

        # Get total count
        count_query = (
            select(func.count())
            .select_from(SessionDocument)
            .where(SessionDocument.session_id == session_id)
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination and sorting by created_at desc
        skip = (page - 1) * limit
        query = (
            query.order_by(SessionDocument.created_at.asc()).offset(skip).limit(limit)
        )

        result = await self.db.execute(query)
        documents = [SessionDocument(**dict(row._mapping)) for row in result]

        return documents, total
