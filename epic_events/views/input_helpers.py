"""Reusable input helpers for terminal views."""

from decimal import Decimal, InvalidOperation
from datetime import datetime
from typing import Optional

from epic_events.views.console import print_error


def ask_int(label: str) -> int:
    """Ask an integer value until input is valid."""

    while True:
        value = input(label).strip()

        try:
            return int(value)

        except ValueError:
            print_error("Valeur invalide. Veuillez entrer un nombre entier.")


def ask_optional_int(label: str) -> Optional[int]:
    """Ask an optional integer value."""

    while True:
        value = input(label).strip()

        if not value:
            return None

        try:
            return int(value)

        except ValueError:
            print_error("Valeur invalide. Veuillez entrer un nombre entier.")


def ask_decimal(label: str) -> Decimal:
    """Ask a decimal value until input is valid."""

    while True:
        value = input(label).strip().replace(",", ".")

        try:
            return Decimal(value)

        except InvalidOperation:
            print_error("Montant invalide. Veuillez entrer un nombre.")


def ask_optional_decimal(label: str) -> Optional[Decimal]:
    """Ask an optional decimal value."""

    while True:
        value = input(label).strip().replace(",", ".")

        if not value:
            return None

        try:
            return Decimal(value)

        except InvalidOperation:
            print_error("Montant invalide. Veuillez entrer un nombre.")


def ask_boolean(label: str) -> bool:
    """Ask a yes/no value until input is valid."""

    while True:
        value = input(label).strip().lower()

        if value in ["o", "oui", "y", "yes", "1"]:
            return True

        if value in ["n", "non", "no", "0"]:
            return False

        print_error("Réponse invalide. Veuillez répondre par oui ou non.")


def ask_optional_boolean(label: str) -> Optional[bool]:
    """Ask an optional yes/no value."""

    while True:
        value = input(label).strip().lower()

        if not value:
            return None

        if value in ["o", "oui", "y", "yes", "1"]:
            return True

        if value in ["n", "non", "no", "0"]:
            return False

        print_error("Réponse invalide. Veuillez répondre par oui ou non.")


def ask_datetime(label: str, date_format: str = "%Y-%m-%d %H:%M") -> datetime:
    """Ask a datetime value until input is valid."""

    while True:
        # value = input(f"{label} ({date_format}) : ").strip()
        value = input(f"{label} : ").strip()

        try:
            return datetime.strptime(value, date_format)

        except ValueError:
            print_error("Date invalide. Format attendu : YYYY-MM-DD HH:MM")


def ask_optional_datetime(
    label: str,
    date_format: str = "%Y-%m-%d %H:%M",
) -> Optional[datetime]:
    """Ask an optional datetime value."""

    while True:
        # value = input(f"{label} ({date_format}) : ").strip()
        value = input(f"{label} : ").strip()

        if not value:
            return None

        try:
            return datetime.strptime(value, date_format)

        except ValueError:
            print_error("Date invalide. Format attendu : YYYY-MM-DD HH:MM")
