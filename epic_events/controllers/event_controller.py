"""Manage event business logic."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from epic_events.controllers.permission_controller import (
    can_assign_support_to_event,
    can_create_event,
    can_delete_event,
    can_update_event,
)
from epic_events.models.model import Contract, Event, User
from epic_events.repositories import event_repository
from epic_events.validators import validate_event_data


def get_all_events(session: Session) -> list[Event]:
    """Return all events."""

    return event_repository.get_all_events(session)


def get_event_by_id(
    session: Session,
    id_event: int,
) -> Optional[Event]:
    """Return an event by id."""

    return event_repository.get_event_by_id(session, id_event)


def get_events_without_support(session: Session) -> list[Event]:
    """Return events without assigned support."""

    return event_repository.get_events_without_support(session)


def get_events_by_support(
    session: Session,
    support_user: User,
) -> list[Event]:
    """Return events assigned to a support user."""

    return event_repository.get_events_by_support(session, support_user)


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

    if not validate_event_data(name, start_date, end_date, location, attendees):
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

    event_repository.save_event(session, event)
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

    try:
        event.assign_support(support_user)

    except ValueError:
        return None

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

    if not validate_event_data(name, start_date, end_date, location, attendees):
        return None

    event.update_event_info(
        name=name,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
    )

    session.commit()

    return event


def delete_event(
    session: Session,
    current_user: User,
    event: Event,
) -> bool:
    """Delete an event if current user is allowed."""

    if not can_delete_event(current_user):
        return False

    return event_repository.delete_event(session, event)
