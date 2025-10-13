from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.lead import Lead
from shared.repositories.base_repository import BaseRepository


class LeadRepository(BaseRepository[Lead]):
    """Repository for lead operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(Lead, db)

    async def get_by_email(self, email: str) -> Optional[Lead]:
        """Get lead by email."""
        result = await self.db.execute(
            select(Lead).where(Lead.email == email),
        )
        return result.scalar_one_or_none()

    async def get_consented_leads(self) -> List[Lead]:
        """Get leads who have given consent."""
        result = await self.db.execute(
            select(Lead).where(Lead.consent == True),  # noqa: E712
        )
        return list(result.scalars().all())

    async def get_leads_with_filters(
        self,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        session_id: Optional[str] = None,
        created_from: Optional[str] = None,
        created_to: Optional[str] = None,
    ) -> Tuple[List[Lead], int]:
        """Get paginated leads with filters.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            search: Search term for email (contains), first name, last name, or phone
            session_id: Filter by session_id
            created_from: Filter by created_at >= this date
            created_to: Filter by created_at <= this date

        Returns:
            Tuple of (leads list, total count)
        """
        # Build base query with selected fields only
        query = select(
            Lead.id,
            Lead.email,
            Lead.first_name,
            Lead.last_name,
            Lead.phone,
            Lead.locale,
            Lead.consent,
            Lead.source,
            Lead.session_id,
            Lead.summary_html,
            Lead.summary_text,
            Lead.annual_switch,
            Lead.created_at,
            Lead.updated_at,
        )

        # Apply filters
        conditions = []

        if search:
            # Search in email, first name, last name, or phone (all case-insensitive contains)
            conditions.append(
                or_(
                    Lead.email.ilike(f"%{search}%"),
                    Lead.first_name.ilike(f"%{search}%"),
                    Lead.last_name.ilike(f"%{search}%"),
                    Lead.phone.ilike(f"%{search}%"),
                ),
            )

        if session_id:
            conditions.append(Lead.session_id == session_id)

        if created_from:
            # Convert string date to datetime object for comparison
            try:
                created_from_date = datetime.strptime(created_from, "%Y-%m-%d")
                conditions.append(Lead.created_at >= created_from_date)
            except ValueError:
                # If parsing fails, skip this filter
                pass

        if created_to:
            # Convert string date to datetime object for comparison
            try:
                created_to_date = datetime.strptime(created_to, "%Y-%m-%d")
                # Add 23:59:59 to include the entire day
                created_to_date = created_to_date.replace(hour=23, minute=59, second=59)
                conditions.append(Lead.created_at <= created_to_date)
            except ValueError:
                # If parsing fails, skip this filter
                pass

        if conditions:
            query = query.where(*conditions)

        # Get total count
        count_query = select(func.count()).select_from(Lead)
        if conditions:
            count_query = count_query.where(*conditions)
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # Apply pagination and sorting
        skip = (page - 1) * limit
        query = query.order_by(Lead.updated_at.desc()).offset(skip).limit(limit)

        result = await self.db.execute(query)
        leads = [Lead(**dict(row._mapping)) for row in result]

        return leads, total
