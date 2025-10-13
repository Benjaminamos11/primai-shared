from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.chat_message import ChatMessage
from shared.models.chat_session import ChatSession
from shared.models.session_document import SessionDocument
from shared.repositories.base_repository import BaseRepository


class ChatSessionRepository(BaseRepository[ChatSession]):
    """Repository for chat session operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(ChatSession, db)

    async def get_sessions_with_filters(
        self,
        page: int = 1,
        limit: int = 10,
        accident: Optional[bool] = None,
        search: Optional[str] = None,
        created_from: Optional[str] = None,
        created_to: Optional[str] = None,
        min_message_count: Optional[int] = None,
    ) -> Tuple[List[ChatSession], int]:
        """Get paginated chat sessions with filters.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            accident: Filter by accident coverage (True/False/None for all)
            search: Search term for email (contains) or exact PLZ match
            created_from: Filter by created_at >= this date
            created_to: Filter by created_at <= this date
            min_message_count: Filter sessions with message count > this value

        Returns:
            Tuple of (sessions list with counts, total count)
        """
        # Build base query with selected fields only
        query = (
            select(
                ChatSession.id,
                ChatSession.plz,
                ChatSession.canton,
                ChatSession.yob,
                ChatSession.age,
                ChatSession.model_pref,
                ChatSession.deductible,
                ChatSession.accident,
                ChatSession.household_json,
                ChatSession.email,
                ChatSession.consent,
                ChatSession.created_at,
                ChatSession.updated_at,
                func.count(ChatMessage.id.distinct()).label("message_count"),
                func.count(SessionDocument.id.distinct()).label("document_count"),
            )
            .outerjoin(
                ChatMessage,
                ChatMessage.session_id == ChatSession.id,
            )
            .outerjoin(
                SessionDocument,
                SessionDocument.session_id == ChatSession.id,
            )
            .group_by(
                ChatSession.id,
            )
        )

        # Apply filters
        conditions = []

        if accident is not None:
            conditions.append(ChatSession.accident == accident)

        if search:
            # Search in email (contains) or exact PLZ match
            conditions.append(
                or_(
                    ChatSession.email.ilike(f"%{search}%"),
                    ChatSession.plz == search,
                ),
            )

        if created_from:
            # Convert string date to datetime object for comparison
            try:
                created_from_date = datetime.strptime(created_from, "%Y-%m-%d")
                conditions.append(ChatSession.created_at >= created_from_date)
            except ValueError:
                # If parsing fails, skip this filter
                pass

        if created_to:
            # Convert string date to datetime object for comparison
            try:
                created_to_date = datetime.strptime(created_to, "%Y-%m-%d")
                # Add 23:59:59 to include the entire day
                created_to_date = created_to_date.replace(hour=23, minute=59, second=59)
                conditions.append(ChatSession.created_at <= created_to_date)
            except ValueError:
                # If parsing fails, skip this filter
                pass

        # If min_message_count is specified, filter sessions with message count > min_message_count
        if min_message_count is not None:
            # Subquery to count messages per session
            message_count_subquery = (
                select(
                    ChatMessage.session_id,
                    func.count(ChatMessage.id).label("message_count"),
                )
                .group_by(ChatMessage.session_id)
                .having(func.count(ChatMessage.id) > min_message_count)
                .subquery()
            )

            # Add join to filter sessions
            query = query.join(
                message_count_subquery,
                ChatSession.id == message_count_subquery.c.session_id,
            )

        if conditions:
            query = query.where(*conditions)

        # Get total count
        count_query = select(func.count()).select_from(ChatSession)

        if min_message_count is not None:
            message_count_subquery = (
                select(
                    ChatMessage.session_id,
                    func.count(ChatMessage.id).label("message_count"),
                )
                .group_by(ChatMessage.session_id)
                .having(func.count(ChatMessage.id) > min_message_count)
                .subquery()
            )
            count_query = count_query.join(
                message_count_subquery,
                ChatSession.id == message_count_subquery.c.session_id,
            )

        if conditions:
            count_query = count_query.where(*conditions)
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination and sorting
        skip = (page - 1) * limit
        query = query.order_by(ChatSession.updated_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        sessions = [dict(row._mapping) for row in result]

        return sessions, total
