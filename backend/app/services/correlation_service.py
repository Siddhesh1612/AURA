"""Business logic for correlated telemetry event groups."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import timedelta
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.models.correlation import Correlation, CorrelationMember
from app.models.enums import CorrelationStatus
from app.models.event import Event
from app.repositories.correlation_repository import CorrelationRepository
from app.repositories.event_repository import EventRepository
from app.schemas.correlation import (
    CorrelationMemberCreate,
    CorrelationMemberResponse,
    CorrelationResponse,
)

__all__ = ["CorrelationService"]

DEFAULT_CORRELATION_WINDOW = timedelta(minutes=5)


class CorrelationService:
    """Orchestrate deterministic event correlation and persistence."""

    def __init__(
        self,
        repository: CorrelationRepository,
        event_repository: EventRepository,
    ) -> None:
        """Initialize the service with repository dependencies."""

        self._repository = repository
        self._event_repository = event_repository

    def correlate_event(self, event_id: UUID) -> CorrelationResponse:
        """Attach an event to a candidate correlation or create one."""

        event = self._event_repository.get_by_id(event_id)
        if event is None:
            raise ValueError("Event does not exist.")

        since = event.occurred_at - DEFAULT_CORRELATION_WINDOW
        candidates = self._repository.list_active_since(since)

        correlation = self._find_candidate(event, candidates)
        if correlation is None:
            correlation = self._create_correlation(event)
        else:
            self._attach_event(
                correlation,
                event,
                "Matched deterministic correlation identifiers.",
            )

        self._repository._session.commit()
        return CorrelationResponse.model_validate(correlation)

    def add_member(
        self,
        correlation_id: UUID,
        member_in: CorrelationMemberCreate,
    ) -> CorrelationMemberResponse:
        """Add an existing event to an existing correlation."""

        correlation = self._repository.get_by_id(correlation_id)
        if correlation is None:
            raise ValueError("Correlation does not exist.")

        event = self._event_repository.get_by_id(member_in.event_id)
        if event is None:
            raise ValueError("Event does not exist.")

        try:
            member = self._attach_event(
                correlation,
                event,
                member_in.membership_reason,
            )
            self._repository._session.commit()
        except IntegrityError:
            self._repository._session.rollback()
            raise ValueError("Event is already a member of this correlation.") from None

        return CorrelationMemberResponse.model_validate(member)

    def _find_candidate(
        self,
        event: Event,
        candidates: Sequence[Correlation],
    ) -> Correlation | None:
        """Return the first candidate sharing deterministic identifiers."""

        for correlation in candidates:
            loaded = self._repository.get_with_members(correlation.id)
            if loaded is None:
                continue

            for member in loaded.members:
                member_event = self._event_repository.get_by_id(member.event_id)
                if member_event is not None and self._events_match(
                    event,
                    member_event,
                ):
                    return loaded

        return None

    def _events_match(self, left: Event, right: Event) -> bool:
        """Return whether events share a stable correlation identity."""

        if (
            left.correlation_key is not None
            and left.correlation_key == right.correlation_key
        ):
            return True

        same_agent = left.agent_id is not None and left.agent_id == right.agent_id
        same_hostname = left.hostname is not None and left.hostname == right.hostname
        same_username = left.username is not None and left.username == right.username

        return same_agent or (same_hostname and same_username)

    def _create_correlation(self, event: Event) -> Correlation:
        """Create a new open correlation containing the given event."""

        correlation = Correlation(
            status=CorrelationStatus.OPEN,
            started_at=event.occurred_at,
            last_activity_at=event.occurred_at,
        )
        persisted = self._repository.create(correlation)

        self._attach_event(
            persisted,
            event,
            "Initial event for correlation.",
        )
        return persisted

    def _attach_event(
        self,
        correlation: Correlation,
        event: Event,
        reason: str,
    ) -> CorrelationMember:
        """Attach an event and update correlation activity."""

        member = CorrelationMember(
            correlation_id=correlation.id,
            event_id=event.id,
            membership_reason=reason,
        )
        persisted = self._repository.add_member(member)

        if event.occurred_at > correlation.last_activity_at:
            correlation.last_activity_at = event.occurred_at

        if correlation.status == CorrelationStatus.OPEN:
            correlation.status = CorrelationStatus.ACTIVE

        return persisted
