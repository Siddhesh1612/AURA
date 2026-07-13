"""Business logic for immutable Event telemetry."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC
from typing import Any

from sqlalchemy.exc import IntegrityError

from app.models.event import Event
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse

__all__ = ["EventService"]


class EventService:
    """Orchestrate Event fingerprinting, deduplication, and persistence."""

    def __init__(self, repository: EventRepository) -> None:
        """Initialize the service with a repository dependency."""

        self._repository = repository

    def create(self, event_in: EventCreate) -> EventResponse:
        """Create or reuse an immutable event record."""

        fingerprint = self._generate_fingerprint(event_in)
        existing = self._repository.get_by_fingerprint(fingerprint)
        if existing is not None:
            return EventResponse.model_validate(existing)

        event = self._build_event(event_in, fingerprint)
        try:
            persisted = self._repository.create(event)
            self._repository._session.commit()
        except IntegrityError:
            self._repository._session.rollback()
            existing = self._repository.get_by_fingerprint(fingerprint)
            if existing is not None:
                return EventResponse.model_validate(existing)
            raise
        return EventResponse.model_validate(persisted)

    def _generate_fingerprint(self, event_in: EventCreate) -> str:
        """Generate a deterministic SHA-256 fingerprint from immutable fields."""

        payload = {
            "source": event_in.source,
            "external_event_id": event_in.external_event_id,
            "event_type": event_in.event_type,
            "occurred_at": event_in.occurred_at.astimezone(UTC).isoformat(),
            "agent_id": event_in.agent_id,
            "hostname": event_in.hostname,
            "username": event_in.username,
            "actor": event_in.actor,
            "target": event_in.target,
            "asset": event_in.asset,
            "raw_payload": event_in.raw_payload,
        }
        canonical = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    def _build_event(self, event_in: EventCreate, fingerprint: str) -> Event:
        """Convert validated schema data into an ORM Event instance."""

        return Event(
            event_fingerprint=fingerprint,
            agent_id=event_in.agent_id,
            hostname=event_in.hostname,
            username=event_in.username,
            source=event_in.source,
            external_event_id=event_in.external_event_id,
            event_type=event_in.event_type,
            severity=event_in.severity,
            occurred_at=event_in.occurred_at,
            actor=event_in.actor,
            target=event_in.target,
            asset=event_in.asset,
            raw_payload=event_in.raw_payload,
            normalized_payload=event_in.normalized_payload,
            enrichment_payload=event_in.enrichment_payload,
        )
