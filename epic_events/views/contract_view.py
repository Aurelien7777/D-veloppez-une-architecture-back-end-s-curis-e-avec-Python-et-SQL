"""Contract terminal views."""

from epic_events.models.model import Contract
from epic_events.views.console import print_info, print_title

from epic_events.views.input_helpers import (
    ask_boolean,
    ask_decimal,
    ask_int,
    ask_optional_boolean,
    ask_optional_decimal,
)


def display_contract_menu() -> str:
    """Display contract menu and return user choice."""

    print_title("MENU CONTRATS")
    print_info("1 - Afficher tous les contrats")
    print_info("2 - Afficher les contrats non signés")
    print_info("3 - Afficher les contrats non payés")
    print_info("4 - Créer un contrat")
    print_info("5 - Modifier un contrat")
    print_info("6 - Supprimer un contrat")
    print_info("0 - Retour")

    return input("\nVotre choix : ")


def display_contracts(contracts: list[Contract]) -> None:
    """Display contracts."""

    if not contracts:
        print_info("Aucun contrat trouvé.")
        return

    for contract in contracts:
        print_info(
            f"[{contract.id_contract}] "
            f"Client : {contract.customer.full_name} | "
            f"Total : {contract.total_amount} € | "
            f"Restant : {contract.remaining_amount} € | "
            f"Signé : {contract.is_signed}"
        )


def ask_contract_id() -> int:
    """Ask contract id."""

    return ask_int("ID du contrat : ")


def ask_contract_customer_id() -> int:
    """Ask customer id for contract creation."""

    return ask_int("ID du client : ")


def ask_contract_data() -> dict:
    """Ask contract creation data."""

    return {
        "total_amount": ask_decimal("Montant total : "),
        "remaining_amount": ask_decimal("Montant restant : "),
        "is_signed": ask_boolean("Contrat signé ? (o/n) : "),
    }


def ask_contract_update_data() -> dict:
    """Ask contract update data."""

    print_info("Laissez vide pour ne pas modifier un champ.")

    return {
        "total_amount": ask_optional_decimal("Nouveau montant total : "),
        "remaining_amount": ask_optional_decimal("Nouveau montant restant : "),
        "is_signed": ask_optional_boolean("Contrat signé ? (o/n) : "),
    }
