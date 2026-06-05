"""Manage customer business logic."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from epic_events.controllers.permission_controller import (
    can_create_customer,
    can_delete_customer,
    can_update_customer,
)
from epic_events.models.model import Customer, User
from epic_events.repositories import customer_repository
from epic_events.validators import validate_customer_data


def get_all_customers(session: Session) -> list[Customer]:
    """Return all customers."""

    return customer_repository.get_all_customers(session)


def get_customer_by_id(
    session: Session,
    id_customer: int,
) -> Optional[Customer]:
    """Return a customer by id."""

    return customer_repository.get_customer_by_id(session, id_customer)


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

    if not validate_customer_data(full_name, email, phone, company_name):
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

    customer_repository.save_customer(session, customer)
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

    if not validate_customer_data(full_name, email, phone, company_name):
        return None

    customer.update_contact_info(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
    )

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

    return customer_repository.delete_customer(session, customer)
