"""Manage user business logic."""

from typing import Optional

from sqlalchemy.orm import Session

from epic_events.controllers.auth_controller import hash_password
from epic_events.controllers.permission_controller import can_manage_users
from epic_events.models.model import Role, User
from epic_events.repositories import user_repository
from epic_events.validators import validate_user_data


def get_all_users(session: Session) -> list[User]:
    """Return all users."""

    return user_repository.get_all_users(session)


def get_user_by_id(
    session: Session,
    id_user: int,
) -> Optional[User]:
    """Return a user by id."""

    return user_repository.get_user_by_id(session, id_user)


def get_role_by_name(
    session: Session,
    role_name: str,
) -> Optional[Role]:
    """Return a role by name."""

    return user_repository.get_role_by_name(session, role_name)


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

    return user_repository.save_user(session, user)


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

    return user_repository.update_user_fields(
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

    return user_repository.delete_user(session, user)
