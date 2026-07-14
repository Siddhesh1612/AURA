"""Pydantic schemas for correlated telemetry event groups."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.enums import CorrelationStatus

__all__ = [
    "CorrelationCreate",
    "CorrelationMemberCreate",
    "CorrelationMemberResponse",
    "CorrelationResponse",
]

MEMBERSHIP_REASON_MAX_LENGTH = 255

MembershipReasonStr = Annotated[
    str,
    Field(min_length=1, max_length=MEMBERSHIP_REASON_MAX_LENGTH),
]


class CorrelationMemberCreate(BaseModel):
    """Validated input for adding an event to a correlation."""

    model_config = ConfigDict(extra="forbid")

    event_id: UUID
    membership_reason: MembershipReasonStr


class CorrelationMemberResponse(BaseModel):
    """Outbound schema for a correlation membership record."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    correlation_id: UUID
    event_id: UUID
    added_at: datetime
    membership_reason: MembershipReasonStr

    @field_validator("added_at")
    @classmethod
    def validate_added_at(cls, value: datetime) -> datetime:
        """Require timezone-aware membership timestamps."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("added_at must be timezone-aware.")
        return value


class CorrelationCreate(BaseModel):
    """Validated input for creating a correlation."""

    model_config = ConfigDict(extra="forbid")

    started_at: datetime
    last_activity_at: datetime

    @field_validator("started_at", "last_activity_at")
    @classmethod
    def validate_timestamps(cls, value: datetime) -> datetime:
        """Require timezone-aware correlation timestamps."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Correlation timestamps must be timezone-aware.")
        return value

    @model_validator(mode="after")
    def validate_timeline(self) -> CorrelationCreate:
        """Ensure correlation activity does not precede its start."""

        if self.last_activity_at < self.started_at:
            raise ValueError(
                "last_activity_at cannot precede started_at."
            )
        return self


class CorrelationResponse(BaseModel):
    """Outbound schema serialized from Correlation ORM objects."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: CorrelationStatus
    started_at: datetime
    last_activity_at: datetime
    closed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    @field_validator(
        "started_at",
        "last_activity_at",
        "created_at",
        "updated_at",
    )
    @classmethod
    def validate_response_timestamps(cls, value: datetime) -> datetime:
        """Require timezone-aware correlation timestamps."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Correlation timestamps must be timezone-aware.")
        return value

    @field_validator("closed_at")
    @classmethod
    def validate_closed_at(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        """Require a timezone-aware closure timestamp when provided."""

        if (
            value is not None
            and (value.tzinfo is None or value.utcoffset() is None)
        ):
            raise ValueError("closed_at must be timezone-aware.")
        return value
    