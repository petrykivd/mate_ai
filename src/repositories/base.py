from abc import ABC

from loguru import logger
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    model = None

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self):
        pass

    async def list(self):
        pass

    async def update(self):
        pass

    async def add(self, obj_data: dict):
        new_obj = await self._session.scalar(
            insert(self.model).values(**obj_data).returning(self.model)
        )
        logger.info(f"Created new obj {new_obj}")
        return new_obj

    async def delete(self):
        pass
