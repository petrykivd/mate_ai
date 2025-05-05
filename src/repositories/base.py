from abc import ABC

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

    async def add(self):
        pass

    async def delete(self):
        pass
