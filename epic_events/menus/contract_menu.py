"""Contract terminal menu."""

from sqlalchemy.orm import Session

from epic_events.controllers.permission_controller import can_create_contract
from epic_events.controllers.contract_controller import (
    create_contract,
    delete_contract,
    get_all_contracts,
    get_contract_by_id,
    get_unpaid_contracts,
    get_unsigned_contracts,
    update_contract,
)
from epic_events.controllers.customer_controller import get_customer_by_id
from epic_events.controllers.token_controller import get_current_user
from epic_events.database import SessionLocal
from epic_events.models.model import User
from epic_events.views.console import print_error, print_success
from epic_events.views.contract_view import (
    ask_contract_customer_id,
    ask_contract_data,
    ask_contract_id,
    ask_contract_update_data,
    display_contract_menu,
    display_contracts,
)

from epic_events.exceptions import EpicEventsError


def show_all_contracts(session: Session) -> None:
    """Display all contracts."""

    contracts = get_all_contracts(session)
    display_contracts(contracts)


def show_unsigned_contracts(session: Session) -> None:
    """Display unsigned contracts."""

    contracts = get_unsigned_contracts(session)
    display_contracts(contracts)


def show_unpaid_contracts(session: Session) -> None:
    """Display unpaid contracts."""

    contracts = get_unpaid_contracts(session)
    display_contracts(contracts)


def create_contract_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask contract data and create a contract."""

    if not can_create_contract(current_user):
        print_error("Seul un membre de la gestion peut créer un contrat.")
        return

    id_customer = ask_contract_customer_id()
    customer = get_customer_by_id(session, id_customer)

    if customer is None:
        print_error("Client introuvable.")
        return

    contract_data = ask_contract_data()

    try:
        create_contract(
            session=session,
            current_user=current_user,
            customer=customer,
            **contract_data,
        )

    except EpicEventsError as error:
        print_error(str(error))
        return

    print_success("Contrat créé avec succès.")


def update_contract_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask contract data and update a contract."""

    id_contract = ask_contract_id()
    contract = get_contract_by_id(session, id_contract)

    if contract is None:
        print_error("Contrat introuvable.")
        return

    update_data = ask_contract_update_data()

    try:
        update_contract(
            session=session,
            current_user=current_user,
            contract=contract,
            **update_data,
        )

    except EpicEventsError as error:
        print_error(str(error))
        return

    print_success("Contrat modifié avec succès.")


def delete_contract_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask contract id and delete a contract."""

    id_contract = ask_contract_id()
    contract = get_contract_by_id(session, id_contract)

    if contract is None:
        print_error("Contrat introuvable.")
        return

    try:
        delete_contract(
            session=session,
            current_user=current_user,
            contract=contract,
        )

    except EpicEventsError as error:
        print_error(str(error))
        return

    print_success("Contrat supprimé avec succès")


def run_contract_menu() -> None:
    """Run contract menu."""

    while True:
        session = SessionLocal()

        try:
            current_user = get_current_user(session)

            if current_user is None:
                print_error("Aucun utilisateur connecté.")
                return

            choice = display_contract_menu()

            if choice == "1":
                show_all_contracts(session)

            elif choice == "2":
                show_unsigned_contracts(session)

            elif choice == "3":
                show_unpaid_contracts(session)

            elif choice == "4":
                create_contract_from_menu(session, current_user)

            elif choice == "5":
                update_contract_from_menu(session, current_user)

            elif choice == "6":
                delete_contract_from_menu(session, current_user)

            elif choice == "0":
                return

            else:
                print_error("Choix invalide.")

        finally:
            session.close()
