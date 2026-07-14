"""ORM models for correlated telemetry event groups."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Final

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db.base import Base
from app.models.enums import CorrelationStatus

__all__ = ["Correlation", "CorrelationMember"]


class Correlation(Base):
    """Aggregate representing a correlated group of telemetry events."""

    __tablename__: Final[str] = "correlations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    status: Mapped[CorrelationStatus] = mapped_column(
        SAEnum(CorrelationStatus, name="correlation_status"),
        nullable=False,
        default=CorrelationStatus.OPEN,
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    closed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    members: Mapped[list[CorrelationMember]] = relationship(
        back_populates="correlation",
        cascade="all, delete-orphan",
    )

    @validates("started_at")
    def validate_started_at(
        self,
        key: str,
        value: datetime,
    ) -> datetime:
        """Ensure correlation start does not follow known activity."""

        if (
            self.last_activity_at is not None
            and value > self.last_activity_at
        ):
            raise ValueError(
                "started_at cannot follow last_activity_at"
            )

        if self.closed_at is not None and value > self.closed_at:
            raise ValueError(
                "started_at cannot follow closed_at"
            )

        return value
    @validates("last_activity_at")
    def validate_last_activity_at(
        self,
        key: str,
        value: datetime,
    ) -> datetime:
        """Ensure activity does not precede correlation start."""

        if self.started_at is not None and value < self.started_at:
            raise ValueError(
                "last_activity_at cannot precede started_at"
            )

        return value

    @validates("closed_at")
    def validate_closed_at(
        self,
        key: str,
        value: datetime | None,
    ) -> datetime | None:
        """Ensure closure does not precede correlation start."""

        if (
            value is not None
            and self.started_at is not None
            and value < self.started_at
        ):
            raise ValueError(
                "closed_at cannot precede started_at"
            )

        return value


class CorrelationMember(Base):
    """Membership record linking an immutable event to a correlation."""

    __tablename__: Final[str] = "correlation_members"
    __table_args__ = (
        UniqueConstraint(
            "correlation_id",
            "event_id",
            name="uq_correlation_members_correlation_event",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    correlation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("correlations.id"),
        nullable=False,
        index=True,
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("events.id"),
        nullable=False,
        index=True,
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    membership_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    correlation: Mapped[Correlation] = relationship(
        back_populates="members",
    )
