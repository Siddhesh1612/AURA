"""Reusable domain enums for ORM models."""

from __future__ import annotations

from enum import Enum

__all__ = ["EventSeverity"]


class EventSeverity(str, Enum):
    """Severity scale for telemetry events."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

