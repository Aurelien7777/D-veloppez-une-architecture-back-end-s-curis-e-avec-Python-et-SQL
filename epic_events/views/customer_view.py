"""Customer terminal views."""

from rich.table import Table

from epic_events.models.model import Customer
from epic_events.views.console import console, print_info, print_title


def display_customer_menu() -> str:
    """Display customer menu."""

    print_title("CLIENTS")
    print_info("1 - Lister les clients")
    print_info("2 - Créer un client")
    print_info("3 - Modifier un client")
    print_info("4 - Supprimer un client")
    print_info("0 - Retour")

    return input("\nVotre choix : ")


def display_customers(customers: list[Customer]) -> None:
    """Display customers in a table."""

    table = Table(title="Clients")
    table.add_column("ID")
    table.add_column("Nom")
    table.add_column("Email")
    table.add_column("Téléphone")
    table.add_column("Entreprise")
    table.add_column("Commercial ID")

    for customer in customers:
        table.add_row(
            str(customer.id_customer),
            customer.full_name,
            customer.email,
            customer.phone,
            customer.company_name,
            str(customer.id_commercial),
        )

    console.print(table)


def ask_customer_data() -> dict[str, str]:
    """Ask data to create a customer."""

    return {
        "full_name": input("Nom complet : "),
        "email": input("Email : "),
        "phone": input("Téléphone : "),
        "company_name": input("Entreprise : "),
    }


def ask_customer_update_data() -> dict[str, str | None]:
    """Ask data to update a customer."""

    print_info("Laisse vide pour ne pas modifier le champ.")

    full_name = input("Nouveau nom complet : ")
    email = input("Nouvel email : ")
    phone = input("Nouveau téléphone : ")
    company_name = input("Nouvelle entreprise : ")

    return {
        "full_name": full_name or None,
        "email": email or None,
        "phone": phone or None,
        "company_name": company_name or None,
    }


def ask_customer_id() -> int:
    """Ask customer id."""

    return int(input("ID client : "))
