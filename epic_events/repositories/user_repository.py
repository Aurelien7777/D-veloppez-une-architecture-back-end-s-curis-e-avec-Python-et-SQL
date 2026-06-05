"""User repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.models.model import Role, User
from epic_events.repositories.base_repository import (
    delete_object,
    get_all,
    get_by_id,
)


def get_all_users(session: Session) -> list[User]:
    """Return all users."""

    return get_all(session, User)


def get_user_by_id(
    session: Session,
    id_user: int,
) -> Optional[User]:
    """Return a user by id."""

    return get_by_id(
        session,
        User,
        User.id_user,
        id_user,
    )


def get_role_by_name(
    session: Session,
    role_name: str,
) -> Optional[Role]:
    """Return a role by name."""

    statement = select(Role).where(Role.name == role_name)
    return session.scalars(statement).first()


def save_user(
    session: Session,
    user: User,
) -> User:
    """Add a user to the current session."""

    session.add(user)

    return user


def delete_user(
    session: Session,
    user: User,
) -> bool:
    """Delete a user."""

    return delete_object(session, user)
