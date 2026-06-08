"""User terminal menu."""

from typing import Optional

from sqlalchemy.orm import Session

from epic_events.exceptions import EpicEventsError
from epic_events.controllers.permission_controller import can_manage_users
from epic_events.controllers.token_controller import get_current_user
from epic_events.controllers.user_controller import (
    create_user,
    delete_user,
    get_all_users,
    get_role_by_name,
    get_user_by_id,
    update_user,
)
from epic_events.database import SessionLocal
from epic_events.models.model import Role, User
from epic_events.views.console import print_error, print_success
from epic_events.views.user_view import (
    ask_user_data,
    ask_user_id,
    ask_user_update_data,
    display_user_menu,
    display_users,
)


def get_role_from_menu(
    session: Session,
    role_name: Optional[str],
) -> Optional[Role]:
    """Return role from role name."""

    if role_name is None:
        return None

    role = get_role_by_name(session, role_name)

    if role is None:
        print_error("Rôle introuvable.")
        return None

    return role


def show_all_users(session: Session) -> None:
    """Display all users."""

    users = get_all_users(session)
    display_users(users)


def create_user_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask user data and create a user."""

    if not can_manage_users(current_user):
        print_error("Seul un membre de la gestion peut créer un utilisateur.")
        return

    user_data = ask_user_data()
    role = get_role_from_menu(session, user_data["role_name"])

    if role is None:
        return

    try:
        create_user(
            session=session,
            current_user=current_user,
            full_name=user_data["full_name"],
            email=user_data["email"],
            employee_number=user_data["employee_number"],
            password=user_data["password"],
            role=role,
        )
    except EpicEventsError as error:
        print_error(str(error))
        return

    print_success("Collaborateur créé avec succès.")


def update_user_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask user data and update a user."""

    if not can_manage_users(current_user):
        print_error("Seul un membre de la gestion peut modifier un utilisateur.")

    id_user = ask_user_id()
    user = get_user_by_id(session, id_user)

    if user is None:
        print_error("Collaborateur introuvable.")
        return

    update_data = ask_user_update_data()
    role = get_role_from_menu(session, update_data["role_name"])

    if update_data["role_name"] is not None and role is None:
        return

    try:
        update_user(
            session=session,
            current_user=current_user,
            user=user,
            full_name=update_data["full_name"],
            email=update_data["email"],
            employee_number=update_data["employee_number"],
            password=update_data["password"],
            role=role,
        )
    except EpicEventsError as error:
        print_error(str(error))
        return

    print_success("Collaborateur modifié avec succès.")


def delete_user_from_menu(
    session: Session,
    current_user: User,
) -> None:
    """Ask user id and delete a user."""

    id_user = ask_user_id()
    user = get_user_by_id(session, id_user)

    if user is None:
        print_error("Collaborateur introuvable.")
        return

    try:
        delete_user(
            session=session,
            current_user=current_user,
            user=user,
        )
    except EpicEventsError as error:
        print_error(str(error))
        return

    print_success("Collaborateur supprimé avec succès.")


def run_user_menu() -> None:
    """Run user menu."""

    while True:
        session = SessionLocal()

        try:
            current_user = get_current_user(session)

            if current_user is None:
                print_error("Aucun utilisateur connecté.")
                return

            choice = display_user_menu()

            if choice == "1":
                show_all_users(session)

            elif choice == "2":
                create_user_from_menu(session, current_user)

            elif choice == "3":
                update_user_from_menu(session, current_user)

            elif choice == "4":
                delete_user_from_menu(session, current_user)

            elif choice == "0":
                return

            else:
                print_error("Choix invalide.")

        finally:
            session.close()
