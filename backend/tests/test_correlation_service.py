"""Unit tests for correlation service decision logic."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from unittest.mock import Mock

import pytest
from app.models.correlation import Correlation, CorrelationMember
from app.models.enums import CorrelationStatus
from app.models.event import Event
from app.services.correlation_service import CorrelationService


def build_event(
    *,
    agent_id: str | None = None,
    hostname: str | None = None,
    username: str | None = None,
    correlation_key: str | None = None,
) -> Event:
    """Build an Event instance for correlation service tests."""

    return Event(
        id=uuid.uuid4(),
        event_fingerprint=uuid.uuid4().hex,
        agent_id=agent_id,
        hostname=hostname,
        username=username,
        source="test",
        external_event_id=None,
        event_type="test_event",
        occurred_at=datetime(2026, 7, 14, 12, 0, tzinfo=UTC),
        actor=None,
        target=None,
        asset=None,
        correlation_key=correlation_key,
        raw_payload={},
        normalized_payload=None,
        enrichment_payload=None,
    )


def build_service() -> CorrelationService:
    """Build a correlation service with mocked repositories."""

    correlation_repository = Mock()
    event_repository = Mock()

    return CorrelationService(
        repository=correlation_repository,
        event_repository=event_repository,
    )


def test_events_match_on_explicit_correlation_key() -> None:
    """Events sharing an explicit correlation key should match."""

    service = build_service()
    left = build_event(correlation_key="attack-chain-1")
    right = build_event(correlation_key="attack-chain-1")

    assert service._events_match(left, right) is True


def test_events_match_on_same_agent() -> None:
    """Events emitted by the same agent should match."""

    service = build_service()
    left = build_event(agent_id="agent-001")
    right = build_event(agent_id="agent-001")

    assert service._events_match(left, right) is True


def test_events_match_on_same_hostname_and_username() -> None:
    """Events sharing host and user identity should match."""

    service = build_service()
    left = build_event(
        hostname="BANK-PC-01",
        username="analyst",
    )
    right = build_event(
        hostname="BANK-PC-01",
        username="analyst",
    )

    assert service._events_match(left, right) is True


def test_events_do_not_match_on_username_alone() -> None:
    """A shared username on different hosts should not match."""

    service = build_service()
    left = build_event(
        hostname="BANK-PC-01",
        username="admin",
    )
    right = build_event(
        hostname="BANK-PC-02",
        username="admin",
    )

    assert service._events_match(left, right) is False


def test_events_do_not_match_without_shared_identity() -> None:
    """Unrelated events should not be correlated."""

    service = build_service()
    left = build_event(
        agent_id="agent-001",
        hostname="BANK-PC-01",
        username="analyst",
    )
    right = build_event(
        agent_id="agent-002",
        hostname="BANK-PC-02",
        username="administrator",
    )

    assert service._events_match(left, right) is False


def test_create_correlation_starts_with_event_timestamp() -> None:
    """A new correlation should use the initial event timeline."""

    service = build_service()
    event = build_event(agent_id="agent-001")

    repository = service._repository
    repository.create.side_effect = lambda correlation: correlation
    repository.add_member.side_effect = lambda member: member

    correlation = service._create_correlation(event)

    assert correlation.status == CorrelationStatus.ACTIVE
    assert correlation.started_at == event.occurred_at
    assert correlation.last_activity_at == event.occurred_at
    repository.create.assert_called_once()


def test_attach_event_updates_last_activity() -> None:
    """A newer member event should advance correlation activity."""

    service = build_service()
    correlation = Correlation(
        id=uuid.uuid4(),
        status=CorrelationStatus.ACTIVE,
        started_at=datetime(2026, 7, 14, 12, 0, tzinfo=UTC),
        last_activity_at=datetime(2026, 7, 14, 12, 0, tzinfo=UTC),
    )
    event = build_event(agent_id="agent-001")
    event.occurred_at = datetime(2026, 7, 14, 12, 3, tzinfo=UTC)

    service._repository.add_member.side_effect = lambda member: member

    member = service._attach_event(
        correlation,
        event,
        "Matched test identity.",
    )

    assert isinstance(member, CorrelationMember)
    assert correlation.last_activity_at == event.occurred_at
    assert member.event_id == event.id


def test_add_member_rejects_missing_correlation() -> None:
    """Manual membership should reject an unknown correlation."""

    service = build_service()
    service._repository.get_by_id.return_value = None

    member_in = Mock()
    member_in.event_id = uuid.uuid4()
    member_in.membership_reason = "Test membership."

    with pytest.raises(
        ValueError,
        match="Correlation does not exist",
    ):
        service.add_member(uuid.uuid4(), member_in)