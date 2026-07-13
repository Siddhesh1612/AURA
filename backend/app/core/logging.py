"""Centralized application logging configuration."""

from __future__ import annotations

import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Final

from app.core.settings import get_settings

__all__ = ["setup_logging", "get_logger"]

LOGGER_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
LOG_FILE_NAME: Final[str] = "aura.log"
LOG_BACKUP_COUNT: Final[int] = 30
HANDLER_MARKER: Final[str] = "_aura_handler"


def _resolve_level(level_name: str) -> int:
    """Convert a configured log level into a logging constant."""

    level = level_name.strip().upper()
    if level.isdigit():
        return int(level)
    return int(getattr(logging, level, logging.INFO))


def _logs_directory() -> Path:
    """Return the project logs directory, creating it if needed."""

    logs_dir = Path(__file__).resolve().parents[2] / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def _mark_handler(handler: logging.Handler) -> None:
    """Tag a handler so repeated initialization stays idempotent."""

    setattr(handler, HANDLER_MARKER, True)


def setup_logging() -> logging.Logger:
    """Configure and return the shared application logger."""

    settings = get_settings()
    level = _resolve_level(settings.log_level)
    formatter = logging.Formatter(LOGGER_FORMAT, datefmt=DATE_FORMAT)
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    existing_handlers = [h for h in root_logger.handlers if getattr(h, HANDLER_MARKER, False)]
    if existing_handlers:
        for handler in existing_handlers:
            handler.setLevel(level)
            handler.setFormatter(formatter)
        return root_logger

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    _mark_handler(console_handler)

    file_handler = TimedRotatingFileHandler(
        _logs_directory() / LOG_FILE_NAME,
        when="midnight",
        interval=1,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
        delay=True,
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    _mark_handler(file_handler)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    return root_logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Return a logger after ensuring the shared configuration is active."""

    setup_logging()
    return logging.getLogger(name)
