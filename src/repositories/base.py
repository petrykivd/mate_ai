from abc import ABC

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
        new_obj = await self._session.execute(
            insert(self.model).values(**obj_data)
        )
        return new_obj

    async def delete(self):
        pass
