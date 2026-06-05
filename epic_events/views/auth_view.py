"""Authentication terminal views."""

from getpass import getpass


def ask_login_credentials() -> tuple[str, str]:
    """Ask user login credentials."""

    email = input("Email: ")
    password = getpass("Password: ")

    return email, password
