from typing import Dict, List, Optional, Tuple

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
    ) -> Tuple[List[Dict], int]:
        """Get paginated chat sessions with filters and counts.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            accident: Filter by accident coverage (True/False/None for all)
            search: Search term for email (contains) or exact PLZ match

        Returns:
            Tuple of (sessions list with counts, total count)
        """
        # Build base query with selected fields and counts
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
                ChatSession.lead_id,
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

        if conditions:
            query = query.where(*conditions)

        # Get total count
        count_query = select(func.count()).select_from(ChatSession)
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
