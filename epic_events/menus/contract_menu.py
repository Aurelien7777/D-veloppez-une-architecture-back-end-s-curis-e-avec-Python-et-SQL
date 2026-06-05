"""Contract terminal menu."""

from sqlalchemy.orm import Session

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

    id_customer = ask_contract_customer_id()
    customer = get_customer_by_id(session, id_customer)

    if customer is None:
        print_error("Client introuvable.")
        return

    contract_data = ask_contract_data()

    contract = create_contract(
        session=session,
        current_user=current_user,
        customer=customer,
        **contract_data,
    )

    if contract is None:
        print_error("Création contrat impossible : permission refusée ou données invalides.")
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

    updated_contract = update_contract(
        session=session,
        current_user=current_user,
        contract=contract,
        **update_data,
    )

    if updated_contract is None:
        print_error("Modification contrat impossible : permission refusée ou données invalides.")
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

    deleted = delete_contract(
        session=session,
        current_user=current_user,
        contract=contract,
    )

    if deleted:
        print_success("Contrat supprimé avec succès.")
        return

    print_error("Suppression contrat refusée.")


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
