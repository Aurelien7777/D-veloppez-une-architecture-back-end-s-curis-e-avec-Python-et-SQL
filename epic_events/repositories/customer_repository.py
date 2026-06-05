"""Customer repository."""

from typing import Optional

from sqlalchemy.orm import Session

from epic_events.models.model import Customer
from epic_events.repositories.base_repository import (
    delete_object,
    get_all,
    get_by_id,
)


def get_all_customers(session: Session) -> list[Customer]:
    """Return all customers."""

    return get_all(session, Customer)


def get_customer_by_id(
    session: Session,
    id_customer: int,
) -> Optional[Customer]:
    """Return a customer by id."""

    return get_by_id(
        session,
        Customer,
        Customer.id_customer,
        id_customer,
    )


def save_customer(
    session: Session,
    customer: Customer,
) -> Customer:
    """Add a customer to the current session."""

    session.add(customer)

    return customer


def delete_customer(
    session: Session,
    customer: Customer,
) -> bool:
    """Delete a customer."""

    return delete_object(session, customer)
