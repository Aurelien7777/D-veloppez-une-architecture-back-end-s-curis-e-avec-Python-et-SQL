"""User terminal views."""

from typing import Optional

from epic_events.models.model import User
from epic_events.views.console import print_info, print_title
from epic_events.views.input_helpers import ask_int

VALID_ROLES = ["management", "commercial", "support"]


def display_user_menu() -> str:
    """Display user menu and return user choice."""

    print_title("MENU COLLABORATEURS")
    print_info("1 - Afficher tous les collaborateurs")
    print_info("2 - Créer un collaborateur")
    print_info("3 - Modifier un collaborateur")
    print_info("4 - Supprimer un collaborateur")
    print_info("0 - Retour")

    return input("\nVotre choix : ")


def display_users(users: list[User]) -> None:
    """Display users."""

    if not users:
        print_info("Aucun collaborateur trouvé.")
        return

    for user in users:
        print_info(
            f"[{user.id_user}] "
            f"{user.full_name} | "
            f"Email : {user.email} | "
            f"Rôle : {user.role.name}"
        )


def ask_user_id() -> int:
    """Ask user id."""

    return ask_int("ID du collaborateur : ")


def ask_role_name() -> str:
    """Ask role name."""

    print_info("Rôles disponibles : management, commercial, support")

    return input("Rôle : ")


def ask_optional_role_name() -> Optional[str]:
    """Ask optional role name."""

    print_info("Laissez vide pour ne pas modifier le rôle.")
    print_info("Rôles disponibles : management, commercial, support")

    role_name = input("Nouveau rôle : ")

    if not role_name:
        return None

    return role_name


def ask_user_data() -> dict:
    """Ask user creation data."""

    return {
        "full_name": input("Nom complet : "),
        "email": input("Email : "),
        "employee_number": input("Numéro employé : "),
        "password": input("Mot de passe : "),
        "role_name": ask_role_name(),
    }


def ask_user_update_data() -> dict:
    """Ask user update data."""

    print_info("Laissez vide pour ne pas modifier un champ.")

    return {
        "full_name": input("Nouveau nom complet : ") or None,
        "email": input("Nouvel email : ") or None,
        "employee_number": input("Nouveau numéro employé : ") or None,
        "password": input("Nouveau mot de passe : ") or None,
        "role_name": ask_optional_role_name(),
    }
