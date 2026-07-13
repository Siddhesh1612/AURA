"""PostgreSQL database engine configuration."""

from __future__ import annotations

from functools import lru_cache
from typing import Final

from sqlalchemy import Engine, create_engine

from app.core.settings import get_settings

__all__ = ["setup_engine", "get_engine"]

DEFAULT_DB_ECHO: Final[bool] = False


def _build_engine() -> Engine:
    """Build a SQLAlchemy engine from validated application settings."""

    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("DATABASE_URL is required to initialize the database engine.")

    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_recycle=settings.db_pool_recycle,
        future=True,
        echo=DEFAULT_DB_ECHO,
    )


@lru_cache(maxsize=1)
def setup_engine() -> Engine:
    """Create and cache the shared SQLAlchemy engine."""

    return _build_engine()


def get_engine() -> Engine:
    """Return the shared SQLAlchemy engine without creating it on import."""

    return setup_engine()
