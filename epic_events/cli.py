"""Epic Events CRM command line entry point."""

import argparse
from getpass import getpass

from epic_events.controllers.auth_controller import authenticate_user
from epic_events.controllers.token_controller import (
    create_token,
    delete_token,
    get_current_user,
    save_token,
)
from epic_events.database import SessionLocal


def login():
    """Authenticate user and save local token."""

    email = input("Email: ")
    password = getpass("Password: ")

    session = SessionLocal()

    try:
        user = authenticate_user(session, email, password)

        if user is None:
            print("Authentication failed.")
            return

        token = create_token(user)
        save_token(token)

        print(f"Authentication successful. Welcome {user.full_name}.")

    finally:
        session.close()


def logout():
    """Delete local authentication token."""

    delete_token()
    print("Logout successful.")


def whoami():
    """Display current authenticated user."""

    session = SessionLocal()

    try:
        user = get_current_user(session)

        if user is None:
            print("No authenticated user.")
            return

        print(f"Authenticated user: {user.full_name}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role.name}")

    finally:
        session.close()


def main():
    """Run Epic Events CLI."""

    parser = argparse.ArgumentParser(description="Epic Events CRM command line application.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("login", help="Authenticate user.")
    subparsers.add_parser("logout", help="Logout current user.")
    subparsers.add_parser("whoami", help="Display current authenticated user.")

    args = parser.parse_args()

    if args.command == "login":
        login()

    elif args.command == "logout":
        logout()

    elif args.command == "whoami":
        whoami()


if __name__ == "__main__":
    main()
