from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
