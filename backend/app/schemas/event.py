"""Pydantic schemas for immutable event telemetry."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import EventSeverity

__all__ = ["EventBase", "EventCreate", "EventResponse"]

SOURCE_MAX_LENGTH = 100
EVENT_TYPE_MAX_LENGTH = 150
IDENTIFIER_MAX_LENGTH = 128
TEXT_MAX_LENGTH = 255

SourceStr = Annotated[str, Field(max_length=SOURCE_MAX_LENGTH)]
EventTypeStr = Annotated[str, Field(max_length=EVENT_TYPE_MAX_LENGTH)]
IdentifierStr = Annotated[str, Field(max_length=IDENTIFIER_MAX_LENGTH)]
TextStr = Annotated[str, Field(max_length=TEXT_MAX_LENGTH)]


class EventBase(BaseModel):
    """Fields shared by event creation and response schemas."""

    model_config = ConfigDict(extra="forbid")

    agent_id: IdentifierStr | None = None
    hostname: TextStr | None = None
    username: TextStr | None = None
    source: SourceStr
    external_event_id: IdentifierStr | None = None
    event_type: EventTypeStr
    severity: EventSeverity = EventSeverity.MEDIUM
    occurred_at: datetime
    actor: TextStr | None = None
    target: TextStr | None = None
    asset: TextStr | None = None
    raw_payload: dict[str, Any]
    normalized_payload: dict[str, Any] | None = None
    enrichment_payload: dict[str, Any] | None = None

    @field_validator("occurred_at")
    @classmethod
    def validate_occurred_at(cls, value: datetime) -> datetime:
        """Require timezone-aware occurrence timestamps."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("occurred_at must be timezone-aware.")
        return value

    @field_validator("raw_payload", "normalized_payload", "enrichment_payload")
    @classmethod
    def validate_payloads(cls, value: dict[str, Any] | None) -> dict[str, Any] | None:
        """Require JSON payloads to be dictionaries when provided."""

        if value is None:
            return None
        if not isinstance(value, dict):
            raise TypeError("Payload fields must be dictionaries.")
        return value


class EventCreate(EventBase):
    """Inbound telemetry schema accepted from clients and agents."""


class EventResponse(EventBase):
    """Outbound telemetry schema serialized from ORM objects."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_fingerprint: IdentifierStr
    created_at: datetime
    ingested_at: datetime

    @field_validator("created_at", "ingested_at")
    @classmethod
    def validate_response_timestamps(cls, value: datetime) -> datetime:
        """Require timezone-aware database timestamps."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Timestamps must be timezone-aware.")
        return value
