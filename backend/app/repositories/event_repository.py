"""Persistence operations for immutable Event telemetry."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Final
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.event import Event

__all__ = ["EventRepository"]


class EventRepository:
    """Database-only repository for Event persistence."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with an active SQLAlchemy session."""

        self._session: Final[Session] = session

    def create(self, event: Event) -> Event:
        """Persist a new event and return the managed ORM instance."""

        self._session.add(event)
        self._session.flush()
        self._session.refresh(event)
        return event

    def get_by_id(self, event_id: UUID) -> Event | None:
        """Return an event by primary key if it exists."""

        return self._session.get(Event, event_id)

    def get_by_fingerprint(self, event_fingerprint: str) -> Event | None:
        """Return an event by its unique fingerprint if it exists."""

        statement: Select[tuple[Event]] = select(Event).where(
            Event.event_fingerprint == event_fingerprint
        )
        return self._session.scalars(statement).first()

    def list(self, limit: int, offset: int) -> Sequence[Event]:
        """Return a paginated list of events ordered by newest ingestion."""

        statement: Select[tuple[Event]] = (
            select(Event)
            .order_by(Event.ingested_at.desc(), Event.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return self._session.scalars(statement).all()

    def exists(self, event_id: UUID) -> bool:
        """Return whether an event exists for the given primary key."""

        return self.get_by_id(event_id) is not None
