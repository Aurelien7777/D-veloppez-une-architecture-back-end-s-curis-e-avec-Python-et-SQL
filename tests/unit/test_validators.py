from datetime import datetime, timedelta
from decimal import Decimal

import pytest

from epic_events.validators import (
    is_valid_date_range,
    is_valid_email,
    is_valid_phone,
    is_valid_role_name,
    validate_contract_data,
    validate_customer_data,
    validate_event_data,
    validate_user_data,
)


@pytest.mark.parametrize(
    "email, expected",
    [
        ("test@example.com", True),
        ("bad-email", False),
        ("test@", False),
        ("", False),
    ],
)
def test_is_valid_email(email, expected):
    assert is_valid_email(email) is expected


@pytest.mark.parametrize(
    "phone, expected",
    [
        ("+33612345678", True),
        ("06 12 34 56 78", True),
        ("123", False),
        ("abc123", False),
        ("", False),
    ],
)
def test_is_valid_phone(phone, expected):
    assert is_valid_phone(phone) is expected


@pytest.mark.parametrize(
    "role_name, expected",
    [
        ("management", True),
        ("commercial", True),
        ("support", True),
        ("admin", False),
    ],
)
def test_is_valid_role_name(role_name, expected):
    assert is_valid_role_name(role_name) is expected


def test_is_valid_date_range():
    start_date = datetime.now()
    end_date = start_date + timedelta(hours=2)

    assert is_valid_date_range(start_date, end_date) is True
    assert is_valid_date_range(end_date, start_date) is False


def test_validate_customer_data():
    assert (
        validate_customer_data(
            full_name="Kevin Casey",
            email="kevin@startup.io",
            phone="0612345678",
            company_name="Cool Startup LLC",
        )
        is True
    )

    assert validate_customer_data(email="bad-email") is False
    assert validate_customer_data(full_name="   ") is False


def test_validate_contract_data():
    assert (
        validate_contract_data(
            total_amount=Decimal("1000.00"),
            remaining_amount=Decimal("500.00"),
        )
        is True
    )

    assert validate_contract_data(total_amount=Decimal("-1.00")) is False
    assert (
        validate_contract_data(
            total_amount=Decimal("500.00"),
            remaining_amount=Decimal("1000.00"),
        )
        is False
    )


def test_validate_event_data():
    start_date = datetime.now() + timedelta(days=1)
    end_date = start_date + timedelta(hours=2)

    assert (
        validate_event_data(
            name="Wedding",
            start_date=start_date,
            end_date=end_date,
            location="Paris",
            attendees=100,
        )
        is True
    )

    assert validate_event_data(name="") is False
    assert validate_event_data(attendees=0) is False
    assert validate_event_data(start_date=end_date, end_date=start_date) is False


def test_validate_user_data():
    assert (
        validate_user_data(
            full_name="Bill Bouquet",
            email="bill@epicevents.com",
            employee_number="EMP001",
            password="Secure123!",
            role_name="management",
        )
        is True
    )

    assert validate_user_data(email="bad-email") is False
    assert validate_user_data(password="short") is False
    assert validate_user_data(role_name="admin") is False


@pytest.mark.parametrize(
    "phone",
    [
        "0612345678",
        "06 12 34 56 78",
        "06-12-34-56-78",
        "+33612345678",
        "+33 6 12 34 56 78",
    ],
)
def test_french_phone_is_valid(phone):
    assert is_valid_phone(phone) is True


@pytest.mark.parametrize(
    "phone",
    [
        "123456",
        "0012345678",
        "+330612345678",
        "+999123456789",
    ],
)
def test_invalid_french_phone_is_invalid(phone):
    assert is_valid_phone(phone) is False
