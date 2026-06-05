"""Main menu terminal view."""

from epic_events.models.model import User
from epic_events.views.console import print_info, print_title


def display_main_menu(user: User) -> str:
    """Display main menu and return user choice."""

    print_title("EPIC EVENTS CRM")

    print_info(f"Connecté : {user.full_name}")
    print_info(f"Rôle : {user.role.name}")
    print_info("")

    print_info("1 - Clients")
    print_info("2 - Contrats")
    print_info("3 - Événements")
    print_info("4 - Collaborateurs")
    print_info("5 - Mon profil")
    print_info("6 - Déconnexion")
    print_info("0 - Quitter")

    return input("\nVotre choix : ")
