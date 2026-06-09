"""Insert initial roles and first management user."""

from getpass import getpass

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from epic_events.controllers.auth_controller import hash_password
from epic_events.database import SessionLocal
from epic_events.models.model import Role, User

ROLE_NAMES = ["management", "commercial", "support"]


def create_roles(session):
    """Create default roles if they do not already exist."""

    for role_name in ROLE_NAMES:
        statement = select(Role).where(Role.name == role_name)
        existing_role = session.scalars(statement).first()

        if existing_role is None:
            role = Role(name=role_name)
            session.add(role)

def management_user_exists(session) -> bool:
    """Return True if at least one management user already exists."""

    statement = (
        select(User)
        .join(Role)
        .where(Role.name == "management")
    )

    return session.scalars(statement).first() is not None


def create_first_management_user(session):
    """Create the first management user."""
    
    if management_user_exists(session):
        print("A management user already exists.")
        return

    email = input("Email: ")
    full_name = input("Full name: ")
    employee_number = input("Employee number: ")
    password = getpass("Password: ")

    statement = select(User).where(User.email == email)
    existing_user = session.scalars(statement).first()

    if existing_user is not None:
        print("User already exists.")
        return

    statement = select(Role).where(Role.name == "management")
    management_role = session.scalars(statement).first()

    user = User(
        full_name=full_name,
        email=email,
        employee_number=employee_number,
        password_hash=hash_password(password),
        role=management_role,
    )

    session.add(user)


def seed_database():
    """Seed database with default roles and first management user."""

    session = SessionLocal()

    try:
        create_roles(session)
        session.commit()

        create_first_management_user(session)
        session.commit()

        print("Database seeded successfully.")

    except SQLAlchemyError as error:
        session.rollback()
        print("Error while seeding database.")
        print(error)

    finally:
        session.close()


if __name__ == "__main__":
    seed_database()
