"""Event terminal views."""

from datetime import datetime
from typing import Optional

from epic_events.models.model import Event
from epic_events.views.console import print_info, print_title

DATE_FORMAT = "%Y-%m-%d %H:%M"


def display_event_menu() -> str:
    """Display event menu and return user choice."""

    print_title("MENU ÉVÉNEMENTS")
    print_info("1 - Afficher tous les événements")
    print_info("2 - Afficher les événements sans support")
    print_info("3 - Afficher mes événements assignés")
    print_info("4 - Créer un événement")
    print_info("5 - Assigner un support à un événement")
    print_info("6 - Modifier un événement")
    print_info("7 - Supprimer un événement")
    print_info("0 - Retour")

    return input("\nVotre choix : ")


def display_events(events: list[Event]) -> None:
    """Display events."""

    if not events:
        print_info("Aucun événement trouvé.")
        return

    for event in events:
        support_name = event.support.full_name if event.support else "Non assigné"

        print_info(
            f"[{event.id_event}] "
            f"{event.name} | "
            f"Client : {event.contract.customer.full_name} | "
            f"Début : {event.start_date} | "
            f"Fin : {event.end_date} | "
            f"Support : {support_name}"
        )


def ask_event_id() -> int:
    """Ask event id."""

    return int(input("ID de l'événement : "))


def ask_event_contract_id() -> int:
    """Ask contract id for event creation."""

    return int(input("ID du contrat : "))


def ask_support_user_id() -> int:
    """Ask support user id."""

    return int(input("ID du collaborateur support : "))


def ask_datetime(label: str) -> datetime:
    """Ask a required datetime."""

    while True:
        value = input(f"{label} ({DATE_FORMAT}) : ")

        try:
            return datetime.strptime(value, DATE_FORMAT)

        except ValueError:
            print_info("Date invalide. Format attendu : YYYY-MM-DD HH:MM")


def ask_optional_datetime(label: str) -> Optional[datetime]:
    """Ask an optional datetime."""

    while True:
        value = input(f"{label} ({DATE_FORMAT}) : ")

        if not value:
            return None

        try:
            return datetime.strptime(value, DATE_FORMAT)

        except ValueError:
            print_info("Date invalide. Format attendu : YYYY-MM-DD HH:MM")


def ask_optional_integer(label: str) -> Optional[int]:
    """Ask an optional integer."""

    value = input(label)

    if not value:
        return None

    return int(value)


def ask_event_data() -> dict:
    """Ask event creation data."""

    return {
        "name": input("Nom de l'événement : "),
        "start_date": ask_datetime("Date de début"),
        "end_date": ask_datetime("Date de fin"),
        "location": input("Lieu : "),
        "attendees": int(input("Nombre de participants : ")),
        "notes": input("Notes : ") or None,
    }


def ask_event_update_data() -> dict:
    """Ask event update data."""

    print_info("Laissez vide pour ne pas modifier un champ.")

    return {
        "name": input("Nouveau nom : ") or None,
        "start_date": ask_optional_datetime("Nouvelle date de début"),
        "end_date": ask_optional_datetime("Nouvelle date de fin"),
        "location": input("Nouveau lieu : ") or None,
        "attendees": ask_optional_integer("Nouveau nombre de participants : "),
        "notes": input("Nouvelles notes : ") or None,
    }
