from fastapi import APIRouter

from src.api.v1.routers.healthcheck import router as healthcheck_router

router = APIRouter()

router.include_router(healthcheck_router)