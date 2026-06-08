"""Event terminal menu."""

from sqlalchemy.orm import Session

from epic_events.exceptions import EpicEventsError
from epic_events.controllers.permission_controller import can_create_event
from epic_events.controllers.contract_controller import get_contract_by_id
from epic_events.controllers.event_controller import (
    assign_support_to_event,
    create_event,
    delete_event,
    get_all_events,
    get_event_by_id,
    get_events_by_support,
    get_events_without_support,
    update_event,
)
from epic_events.controllers.token_controller import get_current_user
from epic_events.controllers.user_controller import get_user_by_id
from epic_events.database import SessionLocal
from epic_events.models.model import User
from epic_events.views.console import print_error, print_success
from epic_events.views.event_view import (
    ask_event_contract_id,
    ask_event_data,
    ask_event_id,
    ask_event_update_data,
    ask_support_user_id,
    display_event_menu,
    display_events,
)


def show_all_events(session: Session) -> None:
    """Display all events."""

    events = get_all_events(session)
    display_events(events)


def show_events_without_support(session: Session) -> None:
    """Display events without support."""

    events = get_events_without_support(session)
    display_events(events)


def show_events_assigned_to_current_user(
    session: Session,
    current_user: User,
) -> None:
    """Display events assigned to current support user."""

    events = get_events_by_support(session, current_user)
    display_events(events)


def create_event_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask event data and create an event."""

    id_contract = ask_event_contract_id()
    contract = get_contract_by_id(session, id_contract)

    if contract is None:
        print_error("Contrat introuvable.")
        return

    event_data = ask_event_data()

    try:
        create_event(
            session=session,
            current_user=current_user,
            contract=contract,
            **event_data,
        )
    except EpicEventsError as error:
        print_error(str(error))

    print_success("Événement créé avec succès.")


def assign_support_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask event and support user ids, then assign support."""

    id_event = ask_event_id()
    event = get_event_by_id(session, id_event)

    if event is None:
        print_error("Événement introuvable.")
        return

    id_support = ask_support_user_id()
    support_user = get_user_by_id(session, id_support)

    if support_user is None:
        print_error("Collaborateur introuvable.")
        return

    try:
        assign_support_to_event(
            session=session,
            current_user=current_user,
            event=event,
            support_user=support_user,
        )
    except EpicEventsError as error:
        print_error(str(error))

    print_success("Support assigné avec succès.")


def update_event_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask event data and update an event."""

    id_event = ask_event_id()
    event = get_event_by_id(session, id_event)

    if event is None:
        print_error("Événement introuvable.")
        return

    update_data = ask_event_update_data()

    try:
        update_event(
        session=session,
        current_user=current_user,
        event=event,
        **update_data,
    )

    except EpicEventsError as error:
        print_error(str(error))
        return

    print_success("Événement modifié avec succès.")


def delete_event_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask event id and delete an event."""

    id_event = ask_event_id()
    event = get_event_by_id(session, id_event)

    if event is None:
        print_error("Événement introuvable.")
        return

    deleted = delete_event(
        session=session,
        current_user=current_user,
        event=event,
    )

    if deleted:
        print_success("Événement supprimé avec succès.")
        return

    print_error("Suppression événement refusée.")


def run_event_menu() -> None:
    """Run event menu."""

    while True:
        session = SessionLocal()

        try:
            current_user = get_current_user(session)

            if current_user is None:
                print_error("Aucun utilisateur connecté.")
                return

            choice = display_event_menu()

            if choice == "1":
                show_all_events(session)

            elif choice == "2":
                show_events_without_support(session)

            elif choice == "3":
                show_events_assigned_to_current_user(session, current_user)

            elif choice == "4":
                create_event_from_menu(session, current_user)

            elif choice == "5":
                assign_support_from_menu(session, current_user)

            elif choice == "6":
                update_event_from_menu(session, current_user)

            elif choice == "7":
                delete_event_from_menu(session, current_user)

            elif choice == "0":
                return

            else:
                print_error("Choix invalide.")

        finally:
            session.close()
