"""Reusable functional test fixtures."""

from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from epic_events.controllers.contract_controller import create_contract
from epic_events.controllers.customer_controller import create_customer
from epic_events.controllers.event_controller import (
    assign_support_to_event,
    create_event,
)


@pytest.fixture
def commercial_customer(test_session, commercial_user):
    """Create a customer assigned to the commercial user."""

    return create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="0678123456",
        company_name="Cool Startup LLC",
    )


@pytest.fixture
def signed_contract(test_session, management_user, commercial_customer):
    """Create a signed contract."""

    return create_contract(
        session=test_session,
        current_user=management_user,
        customer=commercial_customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=True,
    )


@pytest.fixture
def unsigned_contract(test_session, management_user, commercial_customer):
    """Create an unsigned contract."""

    return create_contract(
        session=test_session,
        current_user=management_user,
        customer=commercial_customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )


@pytest.fixture
def contract_factory(test_session, management_user, commercial_customer):
    """Return a helper to create contracts."""

    def _create_contract(
        customer=None,
        current_user=None,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    ):
        return create_contract(
            session=test_session,
            current_user=current_user or management_user,
            customer=customer or commercial_customer,
            total_amount=total_amount,
            remaining_amount=remaining_amount,
            is_signed=is_signed,
        )

    return _create_contract


@pytest.fixture
def event_factory(test_session, commercial_user, signed_contract):
    """Return a helper to create events."""

    def _create_event(
        contract=None,
        current_user=None,
        name="Kevin Casey Wedding",
        start_date=None,
        end_date=None,
        location="Paris",
        attendees=100,
        notes="Wedding event notes.",
    ):
        if start_date is None:
            start_date = datetime.now() + timedelta(days=10)

        if end_date is None:
            end_date = datetime.now() + timedelta(days=11)

        return create_event(
            session=test_session,
            current_user=current_user or commercial_user,
            contract=contract or signed_contract,
            name=name,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
            notes=notes,
        )

    return _create_event


@pytest.fixture
def event(event_factory):
    """Create a default event."""

    return event_factory()


@pytest.fixture
def event_with_support(test_session, management_user, support_user, event):
    """Create an event assigned to a support user."""

    return assign_support_to_event(
        session=test_session,
        current_user=management_user,
        event=event,
        support_user=support_user,
    )
