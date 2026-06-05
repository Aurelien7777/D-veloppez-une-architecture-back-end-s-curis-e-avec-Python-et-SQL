"""Epic Events CRM terminal interface."""

from epic_events.controllers.auth_controller import authenticate_user
from epic_events.controllers.token_controller import (
    create_token,
    delete_token,
    get_current_user,
    save_token,
)
from epic_events.menus.customer_menu import run_customer_menu
from epic_events.menus.contract_menu import run_contract_menu

from epic_events.database import SessionLocal
from epic_events.views.auth_view import ask_login_credentials
from epic_events.views.console import print_error, print_info, print_success, print_title
from epic_events.views.main_menu_view import display_main_menu


def login() -> None:
    """Authenticate user and save token."""

    email, password = ask_login_credentials()
    session = SessionLocal()

    try:
        user = authenticate_user(session, email, password)

        if user is None:
            print_error("Authentication failed.")
            return

        token = create_token(user)
        save_token(token)

        print_success(f"Authentication successful. Welcome {user.full_name}.")

    finally:
        session.close()


def logout() -> None:
    """Delete current token."""

    delete_token()
    print_success("Logout successful.")


def show_profile() -> None:
    """Display current authenticated user."""

    session = SessionLocal()

    try:
        user = get_current_user(session)

        if user is None:
            print_error("No authenticated user.")
            return

        print_title("MON PROFIL")
        print_info(f"Nom : {user.full_name}")
        print_info(f"Email : {user.email}")
        print_info(f"Rôle : {user.role.name}")

    finally:
        session.close()


def run_authenticated_menu() -> None:
    """Run main menu for authenticated user."""

    while True:
        session = SessionLocal()

        try:
            user = get_current_user(session)

            if user is None:
                print_error("Aucun utilisateur connecté.")
                return

            choice = display_main_menu(user)

        finally:
            session.close()

        if choice == "1":
            run_customer_menu()
        elif choice == "2":
            run_contract_menu()
        elif choice == "3":
            print_info("Menu événements à venir.")
        elif choice == "4":
            print_info("Menu collaborateurs à venir.")
        elif choice == "5":
            show_profile()
        elif choice == "6":
            logout()
            return
        elif choice == "0":
            return
        else:
            print_error("Choix invalide.")


def main() -> None:
    """Run Epic Events CRM."""

    while True:
        print_title("EPIC EVENTS CRM")
        print_info("1 - Se connecter")
        print_info("2 - Accéder au CRM")
        print_info("0 - Quitter")

        choice = input("\nVotre choix : ")

        if choice == "1":
            login()
        elif choice == "2":
            run_authenticated_menu()
        elif choice == "0":
            return
        else:
            print_error("Choix invalide.")


if __name__ == "__main__":
    main()
