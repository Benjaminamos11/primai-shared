"""User repository for database operations."""

from typing import Optional

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from shared.models.user import User
from shared.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations."""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email."""
        result = await self.db.execute(
            select(User)
            .options(
                load_only(
                    User.id,
                    User.name,
                    User.email,
                    User.phone,
                    User.role,
                    User.is_active,
                    User.last_active,
                    User.created_at,
                    User.updated_at,
                    User.password,
                ),
            )
            .filter(User.email == email),
        )
        return result.scalar_one_or_none()

    async def is_email_taken(self, email: str) -> bool:
        """Check if an email is already taken."""
        result = await self.db.execute(
            select(exists().where(User.email == email)),
        )
        return result.scalar()

    async def update_user(self, user_id: str, update_data: dict) -> Optional[User]:
        """Update user by ID with dict data."""
        user = await self.get_by_id(user_id)
        if not user:
            return None

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def create_user(self, user_data: dict) -> User:
        """Create a new user."""
        user = User(**user_data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
