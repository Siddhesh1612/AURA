"""Persistence operations for correlated telemetry event groups."""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Final
from uuid import UUID

from app.models.correlation import Correlation, CorrelationMember
from app.models.enums import CorrelationStatus
from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

__all__ = ["CorrelationRepository"]


class CorrelationRepository:
    """Database-only repository for Correlation persistence."""

    def __init__(self, session: Session) -> None:
        """Initialize the repository with an active SQLAlchemy session."""

        self._session: Final[Session] = session

    def create(self, correlation: Correlation) -> Correlation:
        """Persist a new correlation and return the managed ORM instance."""

        self._session.add(correlation)
        self._session.flush()
        self._session.refresh(correlation)
        return correlation

    def get_by_id(self, correlation_id: UUID) -> Correlation | None:
        """Return a correlation by primary key if it exists."""

        return self._session.get(Correlation, correlation_id)

    def get_with_members(
        self,
        correlation_id: UUID,
    ) -> Correlation | None:
        """Return a correlation with its membership records loaded."""

        statement: Select[tuple[Correlation]] = (
            select(Correlation)
            .options(selectinload(Correlation.members))
            .where(Correlation.id == correlation_id)
        )
        return self._session.scalars(statement).first()

    def add_member(
        self,
        member: CorrelationMember,
    ) -> CorrelationMember:
        """Persist a correlation membership record."""

        self._session.add(member)
        self._session.flush()
        self._session.refresh(member)
        return member

    def list_active_since(
        self,
        since: datetime,
    ) -> Sequence[Correlation]:
        """Return non-closed correlations active since the given timestamp."""

        statement: Select[tuple[Correlation]] = (
            select(Correlation)
            .where(
                Correlation.status != CorrelationStatus.CLOSED,
                Correlation.last_activity_at >= since,
            )
            .order_by(
                Correlation.last_activity_at.desc(),
                Correlation.id.desc(),
            )
        )
        return self._session.scalars(statement).all()

    def list(self, limit: int, offset: int) -> Sequence[Correlation]:
        """Return a paginated list of correlations by latest activity."""

        statement: Select[tuple[Correlation]] = (
            select(Correlation)
            .order_by(
                Correlation.last_activity_at.desc(),
                Correlation.id.desc(),
            )
            .limit(limit)
            .offset(offset)
        )
        return self._session.scalars(statement).all()

    def exists(self, correlation_id: UUID) -> bool:
        """Return whether a correlation exists for the given primary key."""

        return self.get_by_id(correlation_id) is not None