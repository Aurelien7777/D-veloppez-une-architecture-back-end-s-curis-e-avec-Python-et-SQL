from datetime import datetime
from decimal import Decimal

import pytest

from epic_events.models.model import Contract, Customer, Event, Role, User


@pytest.fixture
def user_factory():
    """Return a function that creates users for unit tests."""

    def create_user(role_name: str, id_user: int = 1) -> User:
        role = Role(name=role_name)

        return User(
            id_user=id_user,
            full_name="Test User",
            email=f"user{id_user}@test.com",
            employee_number=f"EMP{id_user}",
            password_hash="hashed_password",
            role=role,
        )

    return create_user


@pytest.fixture
def customer_factory():
    """Return a function that creates customers for unit tests."""

    def create_customer(id_commercial: int) -> Customer:
        return Customer(
            full_name="Test Customer",
            email="customer@test.com",
            phone="+33600000000",
            company_name="Test Company",
            created_at=datetime.now(),
            id_commercial=id_commercial,
        )

    return create_customer


@pytest.fixture
def contract_factory():
    """Return a function that creates contracts for unit tests."""

    def create_contract(
        customer: Customer,
        is_signed: bool = True,
    ) -> Contract:
        return Contract(
            total_amount=Decimal("1000.00"),
            remaining_amount=Decimal("500.00"),
            created_at=datetime.now(),
            is_signed=is_signed,
            customer=customer,
        )

    return create_contract


@pytest.fixture
def event_factory():
    """Return a function that creates events for unit tests."""

    def create_event(id_support: int) -> Event:
        return Event(
            name="Test Event",
            start_date=datetime.now(),
            end_date=datetime.now(),
            location="Paris",
            attendees=100,
            id_contract=1,
            id_support=id_support,
        )

    return create_event
