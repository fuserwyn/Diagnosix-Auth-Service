from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ModelType = TypeVar("ModelType")


class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, id: int) -> ModelType:
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj: ModelType):
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(self, db: AsyncSession, db_obj: ModelType, update_data: dict):
        for key, value in update_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj