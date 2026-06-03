"""Manage event business logic"""

from datetime import datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session
from epic_events.controllers.permission_controller import (
    can_create_event,
    can_update_event,
)
from epic_events.models.model import Customer, User, Event


def get_all_event(session: Session) -> list[Event]:
    """Return event."""

    statement = select(Event)
    return list(session.scalars(statement).all())


def get_contract_by_id(
    session: Session,
    id_event: int,
) -> Optional[Event]:
    """Return a event by id."""

    statement = select(Event).where(Event.id_event == id_event)
    return session.scalars(statement).first()
