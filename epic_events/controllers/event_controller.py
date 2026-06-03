"""Manage event business logic."""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.controllers.crud_controller import (
    delete_object,
    get_all,
    get_by_id,
    update_fields,
)
from epic_events.controllers.permission_controller import (
    can_assign_support_to_event,
    can_create_event,
    can_delete_event,
    can_update_event,
)
from epic_events.models.model import Contract, Event, User


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


def create_event(
    session: Session,
    current_user: User,
    contract: Contract,
    name: str,
    start_date: datetime,
    end_date: datetime,
    location: str,
    attendees: int,
    notes: Optional[str] = None,
) -> Optional[Event]:
    """Create an event for a signed contract."""

    if not can_create_event(current_user, contract):
        return None

    if contract.event is not None:
        return None

    event = Event(
        name=name,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        contract=contract,
        support=None,
    )

    session.add(event)
    session.commit()

    return event


def assign_support_to_event(
    session: Session,
    current_user: User,
    event: Event,
    support_user: User,
) -> Optional[Event]:
    """Assign a support user to an event."""

    if not can_assign_support_to_event(current_user):
        return None

    if not support_user.is_support():
        return None

    event.support = support_user
    session.commit()

    return event


def update_event(
    session: Session,
    current_user: User,
    event: Event,
    name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    location: Optional[str] = None,
    attendees: Optional[int] = None,
    notes: Optional[str] = None,
) -> Optional[Event]:
    """Update selected event fields if current user is allowed."""

    if not can_update_event(current_user, event):
        return None

    return update_fields(
        session,
        event,
        name=name,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
    )


def delete_event(
    session: Session,
    current_user: User,
    event: Event,
) -> bool:
    """Delete an event if current user is allowed."""

    if not can_delete_event(current_user):
        return False

    return delete_object(session, event)