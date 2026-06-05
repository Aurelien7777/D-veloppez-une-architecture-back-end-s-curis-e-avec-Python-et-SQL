"""Event repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.models.model import Event, User
from epic_events.repositories.base_repository import (
    delete_object,
    get_all,
    get_by_id,
)


def get_all_events(session: Session) -> list[Event]:
    """Return all events."""

    return get_all(session, Event)


def get_event_by_id(
    session: Session,
    id_event: int,
) -> Optional[Event]:
    """Return an event by id."""

    return get_by_id(
        session,
        Event,
        Event.id_event,
        id_event,
    )


def get_events_without_support(session: Session) -> list[Event]:
    """Return events without assigned support."""

    statement = select(Event).where(Event.id_support.is_(None))
    return list(session.scalars(statement).all())


def get_events_by_support(
    session: Session,
    support_user: User,
) -> list[Event]:
    """Return events assigned to a support user."""

    statement = select(Event).where(Event.id_support == support_user.id_user)
    return list(session.scalars(statement).all())


def save_event(
    session: Session,
    event: Event,
) -> Event:
    """Add an event."""

    session.add(event)

    return event


def delete_event(
    session: Session,
    event: Event,
) -> bool:
    """Delete an event."""

    return delete_object(session, event)
