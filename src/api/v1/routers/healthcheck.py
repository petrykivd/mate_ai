from fastapi import APIRouter

from src.database.core.config import DatabaseSettings

router = APIRouter(tags=["Healthcheck"])


@router.get("/healthcheck")
async def healthcheck():
    """
        Returns health check status
    """

    print(DatabaseSettings())
    return {"status": "ok"}
