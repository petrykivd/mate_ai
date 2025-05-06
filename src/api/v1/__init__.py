from fastapi import APIRouter

from src.api.v1.routers.healthcheck import router as healthcheck_router
from src.api.v1.routers.user import router as user_router


router = APIRouter()

router.include_router(healthcheck_router)
router.include_router(user_router)