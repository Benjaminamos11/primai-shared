from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.email_log import EmailLog
from shared.repositories.base_repository import BaseRepository


class EmailLogRepository(BaseRepository[EmailLog]):
    """Repository for email log operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(EmailLog, db)

    async def get_by_provider_id(self, provider_id: str) -> Optional[EmailLog]:
        """Get email log by provider ID."""
        result = await self.db.execute(
            select(EmailLog).where(EmailLog.provider_id == provider_id),
        )
        return result.scalar_one_or_none()

    async def get_logs_with_filters(
        self,
        page: int = 1,
        limit: int = 10,
        status: Optional[str] = None,
    ) -> Tuple[List[EmailLog], int]:
        """Get paginated email logs with filters.

        Args:
            page: Page number (1-indexed)
            limit: Items per page
            status: Filter by status

        Returns:
            Tuple of (email logs list, total count)
        """
        skip = (page - 1) * limit

        # Build query
        query = select(EmailLog)
        if status:
            query = query.where(EmailLog.status == status)

        query = query.order_by(desc(EmailLog.created_at)).offset(skip).limit(limit)

        result = await self.db.execute(query)
        logs = list(result.scalars().all())

        # Get total count
        count_query = select(func.count(EmailLog.id))
        if status:
            count_query = count_query.where(EmailLog.status == status)

        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        return logs, total

    async def get_analytics(self, days: int = 30) -> Dict:
        """Get email analytics for the specified number of days.

        Args:
            days: Number of days to analyze

        Returns:
            Dictionary with analytics data
        """
        # Date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Total emails
        total_result = await self.db.execute(
            select(func.count(EmailLog.id)).where(
                EmailLog.created_at >= start_date,
            ),
        )
        total_emails = total_result.scalar() or 0

        # Sent emails
        sent_result = await self.db.execute(
            select(func.count(EmailLog.id))
            .where(EmailLog.created_at >= start_date)
            .where(EmailLog.status == "sent"),
        )
        sent_emails = sent_result.scalar() or 0

        # Failed emails
        failed_result = await self.db.execute(
            select(func.count(EmailLog.id))
            .where(EmailLog.created_at >= start_date)
            .where(EmailLog.status == "failed"),
        )
        failed_emails = failed_result.scalar() or 0

        # Pending emails
        pending_result = await self.db.execute(
            select(func.count(EmailLog.id))
            .where(EmailLog.created_at >= start_date)
            .where(EmailLog.status == "pending"),
        )
        pending_emails = pending_result.scalar() or 0

        # Success rate
        success_rate = (sent_emails / total_emails * 100) if total_emails > 0 else 0

        # Emails by template
        template_result = await self.db.execute(
            select(EmailLog.template, func.count(EmailLog.id))
            .where(EmailLog.created_at >= start_date)
            .where(EmailLog.template.isnot(None))
            .group_by(EmailLog.template),
        )
        emails_by_template = {
            template: count for template, count in template_result.fetchall()
        }

        # Emails by day
        daily_result = await self.db.execute(
            select(
                func.date(EmailLog.created_at).label("date"),
                func.count(EmailLog.id).label("count"),
            )
            .where(EmailLog.created_at >= start_date)
            .group_by(func.date(EmailLog.created_at))
            .order_by("date"),
        )
        emails_by_day = [
            {"date": str(date), "count": count}
            for date, count in daily_result.fetchall()
        ]

        # Recent emails
        recent_result = await self.db.execute(
            select(EmailLog)
            .where(EmailLog.created_at >= start_date)
            .order_by(desc(EmailLog.created_at))
            .limit(10),
        )
        recent_emails = [
            {
                "id": log.id,
                "to_email": log.to_email,
                "subject": log.subject,
                "status": log.status,
                "template": log.template,
                "created_at": log.created_at.isoformat(),
            }
            for log in recent_result.scalars().all()
        ]

        return {
            "total_emails": total_emails,
            "sent_emails": sent_emails,
            "failed_emails": failed_emails,
            "pending_emails": pending_emails,
            "success_rate": round(success_rate, 2),
            "emails_by_template": emails_by_template,
            "emails_by_day": emails_by_day,
            "recent_emails": recent_emails,
        }
