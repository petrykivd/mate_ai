from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core.engine import get_async_session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
