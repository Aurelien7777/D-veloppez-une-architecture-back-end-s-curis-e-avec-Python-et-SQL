"""Manage user business logic."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.controllers.auth_controller import hash_password
from epic_events.controllers.crud_controller import (
    delete_object,
    get_all,
    get_by_id,
    update_fields,
)
from epic_events.controllers.permission_controller import can_manage_users
from epic_events.validators import validate_user_data
from epic_events.models.model import Role, User


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


def create_user(
    session: Session,
    current_user: User,
    full_name: str,
    email: str,
    employee_number: str,
    password: str,
    role: Role,
) -> Optional[User]:
    """Create a user if current user is allowed."""

    if not can_manage_users(current_user):
        return None
    
    if not validate_user_data(
        full_name,
        email,
        employee_number,
        password,
        role.name,
    ):
        return None

    user = User(
        full_name=full_name,
        email=email,
        employee_number=employee_number,
        password_hash=hash_password(password),
        role=role,
    )

    session.add(user)
    session.commit()

    return user


def update_user(
    session: Session,
    current_user: User,
    user: User,
    full_name: Optional[str] = None,
    email: Optional[str] = None,
    employee_number: Optional[str] = None,
    password: Optional[str] = None,
    role: Optional[Role] = None,
) -> Optional[User]:
    """Update selected user fields if current user is allowed."""

    if not can_manage_users(current_user):
        return None

    if not validate_user_data(
        full_name,
        email,
        employee_number,
        password,
        role.name if role else None,
    ):
        return None

    password_hash = None

    if password is not None:
        password_hash = hash_password(password)

    return update_fields(
        session,
        user,
        full_name=full_name,
        email=email,
        employee_number=employee_number,
        password_hash=password_hash,
        role=role,
    )


def delete_user(
    session: Session,
    current_user: User,
    user: User,
) -> bool:
    """Delete a user if current user is allowed."""

    if not can_manage_users(current_user):
        return False

    if current_user.id_user == user.id_user:
        return False

    return delete_object(session, user)
