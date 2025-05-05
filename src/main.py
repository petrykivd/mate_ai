from fastapi import FastAPI

from src.api.v1 import router as v1_router

app = FastAPI(
    title="AI Interview Assistant",
    description="Tech check via LLM",
    version="0.1.0",
)

app.include_router(v1_router)
