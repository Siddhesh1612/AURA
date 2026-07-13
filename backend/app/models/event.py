"""ORM model for immutable telemetry events."""

from __future__ import annotations

from datetime import datetime
import uuid
from typing import Any, Final

from sqlalchemy import DateTime, Enum as SAEnum, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.enums import EventSeverity

__all__ = ["Event"]


class Event(Base):
    """Immutable event telemetry captured by AURA."""

    __tablename__: Final[str] = "events"
    __table_args__ = (
        UniqueConstraint("event_fingerprint", name="uq_events_event_fingerprint"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    event_fingerprint: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    agent_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    hostname: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    external_event_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    event_type: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    severity: Mapped[EventSeverity] = mapped_column(
        SAEnum(EventSeverity, name="event_severity"),
        nullable=False,
        default=EventSeverity.MEDIUM,
        index=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    actor: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    target: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    asset: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    correlation_key: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    normalized_payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    enrichment_payload: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
