"""Manage customer business logic."""

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.controllers.permission_controller import (
    can_create_customer,
    can_update_customer,
    can_delete_customer
)
from epic_events.models.model import Customer, User


def get_all_customers(session: Session) -> list[Customer]:
    """Return all customers."""

    statement = select(Customer)
    return list(session.scalars(statement).all())


def get_customer_by_id(
    session: Session,
    id_customer: int,
) -> Optional[Customer]:
    """Return a customer by id."""

    statement = select(Customer).where(Customer.id_customer == id_customer)
    return session.scalars(statement).first()


def create_customer(
    session: Session,
    current_user: User,
    full_name: str,
    email: str,
    phone: str,
    company_name: str,
) -> Optional[Customer]:
    """Create a customer assigned to the current commercial user."""

    if not can_create_customer(current_user):
        return None

    customer = Customer(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        created_at=datetime.now(),
        updated_at=None,
        id_commercial=current_user.id_user,
    )

    session.add(customer)
    session.commit()

    return customer


def update_customer(
    session: Session,
    current_user: User,
    customer: Customer,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    company_name: Optional[str] = None,
) -> Optional[Customer]:
    """Update selected customer fields if current user is allowed."""

    if not can_update_customer(current_user, customer):
        return None

    if full_name is not None:
        customer.full_name = full_name

    if email is not None:
        customer.email = email

    if phone is not None:
        customer.phone = phone

    if company_name is not None:
        customer.company_name = company_name

    customer.updated_at = datetime.now()

    session.commit()

    return customer


def delete_customer(
    session: Session,
    current_user: User,
    customer: Customer,
) -> bool:
    """Delete a customer if current user is allowed."""

    if not can_delete_customer(current_user):
        return False

    session.delete(customer)
    session.commit()

    return True