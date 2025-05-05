from fastapi import APIRouter


router = APIRouter(tags=["Healthcheck"])


@router.get("/healthcheck")
async def healthcheck():
    """
        Returns health check status
    """
    return {"status": "ok"}
