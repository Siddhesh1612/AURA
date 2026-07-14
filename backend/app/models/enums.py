"""Reusable domain enums for ORM models."""

from __future__ import annotations

from enum import Enum

__all__ = ["CorrelationStatus", "EventSeverity"]


class CorrelationStatus(str, Enum):
    """Lifecycle status for correlated event groups."""

    OPEN = "open"
    ACTIVE = "active"
    CLOSED = "closed"


class EventSeverity(str, Enum):
    """Severity scale for telemetry events."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

