"""HTTP endpoints for immutable Event telemetry."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


def _get_event_repository(db: Annotated[Session, Depends(get_db)]) -> EventRepository:
    """Return an EventRepository bound to the current database session."""

    return EventRepository(db)


def _get_event_service(
    repository: Annotated[EventRepository, Depends(_get_event_repository)],
) -> EventService:
    """Return the EventService composed with its repository dependency."""

    return EventService(repository)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    event_in: EventCreate,
    service: Annotated[EventService, Depends(_get_event_service)],
) -> EventResponse:
    """Create an immutable telemetry event or return the existing one."""

    return service.create(event_in)

