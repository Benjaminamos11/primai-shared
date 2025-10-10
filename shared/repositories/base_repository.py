"""Base repository with common CRUD operations."""

from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Base repository with common database operations."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: str) -> Optional[ModelType]:
        """Get record by ID."""
        return await self.db.get(self.model, id)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """Get all records with pagination."""
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit),
        )
        return list(result.scalars().all())

    async def create(self, **kwargs) -> ModelType:
        """Create new record."""
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def bulk_create(self, items: List[dict]) -> List[ModelType]:
        """Create multiple records in a single transaction.

        Args:
            items: List of dictionaries with model fields

        Returns:
            List of created model instances
        """
        instances = [self.model(**item) for item in items]
        self.db.add_all(instances)
        await self.db.commit()
        # Refresh all instances to get generated IDs and timestamps
        for instance in instances:
            await self.db.refresh(instance)
        return instances

    async def update(self, id: str, **kwargs) -> Optional[ModelType]:
        """Update record by ID."""
        instance = await self.get_by_id(id)
        if not instance:
            return None

        for key, value in kwargs.items():
            setattr(instance, key, value)

        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def delete(self, id: str) -> bool:
        """Delete record by ID."""
        instance = await self.get_by_id(id)
        if not instance:
            return False

        await self.db.delete(instance)
        await self.db.commit()
        return True
