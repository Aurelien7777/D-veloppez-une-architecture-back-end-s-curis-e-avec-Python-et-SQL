"""Validate user input before business logic."""

import re
from datetime import datetime
from decimal import Decimal
from typing import Optional

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9\s\-().]{6,30}$")
FRENCH_PHONE_PATTERN = re.compile(r"^(?:0[1-9]\d{8}|\+33[1-9]\d{8})$")
VALID_ROLES = {"management", "commercial", "support"}


def is_not_empty(value: str) -> bool:
    """Return True if value is not empty."""

    return bool(value and value.strip())


def is_valid_email(email: str) -> bool:
    """Return True if email has a valid basic format."""

    return bool(email and EMAIL_PATTERN.match(email))


def is_valid_phone(phone: str) -> bool:
    """Return True if phone has a valid basic format."""
    if not phone:
        return False

    normalized_phone = normalize_phone(phone)

    return bool(FRENCH_PHONE_PATTERN.match(normalized_phone))


def normalize_phone(phone: str) -> str:
    """Return phone number without common separators."""

    return re.sub(r"[\s\-().]", "", phone)


def is_positive_decimal(value: Decimal) -> bool:
    """Return True if decimal value is positive or zero."""

    return value >= 0


def is_positive_integer(value: int) -> bool:
    """Return True if integer value is strictly positive."""

    return value > 0


def is_valid_date_range(start_date: datetime, end_date: datetime) -> bool:
    """Return True if end date is after start date."""

    return end_date > start_date


def is_future_date(value: datetime) -> bool:
    """Return True if date is in the future."""

    return value > datetime.now()


def is_valid_role_name(role_name: str) -> bool:
    """Return True if role name is allowed."""

    return role_name in VALID_ROLES


def validate_customer_data(
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    company_name: Optional[str] = None,
) -> bool:
    """Validate customer fields."""

    if full_name is not None and not is_not_empty(full_name):
        return False

    if email is not None and not is_valid_email(email):
        return False

    if phone is not None and not is_valid_phone(phone):
        return False

    if company_name is not None and not is_not_empty(company_name):
        return False

    return True


def validate_contract_data(
    total_amount: Optional[Decimal] = None,
    remaining_amount: Optional[Decimal] = None,
) -> bool:
    """Validate contract fields."""

    if total_amount is not None and not is_positive_decimal(total_amount):
        return False

    if remaining_amount is not None and not is_positive_decimal(remaining_amount):
        return False

    if (
        total_amount is not None
        and remaining_amount is not None
        and remaining_amount > total_amount
    ):
        return False

    return True


def validate_event_data(
    name: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    location: Optional[str] = None,
    attendees: Optional[int] = None,
) -> bool:
    """Validate event fields."""

    if name is not None and not is_not_empty(name):
        return False

    if location is not None and not is_not_empty(location):
        return False

    if attendees is not None and not is_positive_integer(attendees):
        return False

    if start_date is not None and end_date is not None:
        if not is_valid_date_range(start_date, end_date):
            return False

    if start_date is not None and not is_future_date(start_date):
        return False

    return True


def validate_user_data(
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    employee_number: Optional[str] = None,
    password: Optional[str] = None,
    role_name: Optional[str] = None,
) -> bool:
    """Validate user fields."""

    if full_name is not None and not is_not_empty(full_name):
        return False

    if email is not None and not is_valid_email(email):
        return False

    if employee_number is not None and not is_not_empty(employee_number):
        return False

    if password is not None and len(password) < 8:
        return False

    if role_name is not None and not is_valid_role_name(role_name):
        return False

    return True
