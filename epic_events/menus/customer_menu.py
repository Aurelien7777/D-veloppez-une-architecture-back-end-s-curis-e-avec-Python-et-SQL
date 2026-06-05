"""Customer terminal menu."""

from sqlalchemy.orm import Session

from epic_events.controllers.customer_controller import (
    create_customer,
    delete_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer,
)
from epic_events.controllers.token_controller import get_current_user
from epic_events.database import SessionLocal
from epic_events.models.model import User
from epic_events.views.console import print_error, print_success
from epic_events.views.customer_view import (
    ask_customer_data,
    ask_customer_id,
    ask_customer_update_data,
    display_customer_menu,
    display_customers,
)


def show_all_customers(session: Session) -> None:
    """Display all customers."""

    customers = get_all_customers(session)
    display_customers(customers)


def create_customer_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask customer data and create a customer."""

    customer_data = ask_customer_data()

    customer = create_customer(
        session=session,
        current_user=current_user,
        **customer_data,
    )

    if customer is None:
        print_error("Création client refusée ou données invalides.")
        return

    print_success("Client créé avec succès.")


def update_customer_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask customer data and update a customer."""

    id_customer = ask_customer_id()
    customer = get_customer_by_id(session, id_customer)

    if customer is None:
        print_error("Client introuvable.")
        return

    update_data = ask_customer_update_data()

    updated_customer = update_customer(
        session=session,
        current_user=current_user,
        customer=customer,
        **update_data,
    )

    if updated_customer is None:
        print_error("Modification refusée ou données invalides.")
        return

    print_success("Client modifié avec succès.")


def delete_customer_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask customer id and delete a customer."""

    id_customer = ask_customer_id()
    customer = get_customer_by_id(session, id_customer)

    if customer is None:
        print_error("Client introuvable.")
        return

    deleted = delete_customer(
        session=session,
        current_user=current_user,
        customer=customer,
    )

    if deleted:
        print_success("Client supprimé avec succès.")
        return

    print_error("Suppression refusée.")


def run_customer_menu() -> None:
    """Run customer menu."""

    while True:
        session = SessionLocal()

        try:
            current_user = get_current_user(session)

            if current_user is None:
                print_error("Aucun utilisateur connecté.")
                return

            choice = display_customer_menu()

            if choice == "1":
                show_all_customers(session)

            elif choice == "2":
                create_customer_from_menu(session, current_user)

            elif choice == "3":
                update_customer_from_menu(session, current_user)

            elif choice == "4":
                delete_customer_from_menu(session, current_user)

            elif choice == "0":
                return

            else:
                print_error("Choix invalide.")

        finally:
            session.close()
