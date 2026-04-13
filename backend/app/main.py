from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.endpoints.health import router as health_router
from backend.app.api.v1.endpoints.rag import router as rag_router
from backend.app.core.logging import configure_logging
from backend.app.core.settings import get_settings

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(rag_router, prefix="/api/v1")
