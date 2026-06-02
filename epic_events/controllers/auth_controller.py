from typing import Optional

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.models.model import User

password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plain text password."""

    return password_hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    """Verify a plain text password against a password hash."""

    try:
        return password_hasher.verify(password_hash, password)

    except (VerifyMismatchError, VerificationError):
        return False


def authenticate_user(
    session: Session,
    email: str,
    password: str,
) -> Optional[User]:
    """Authenticate a user with email and password."""

    statement = select(User).where(User.email == email)
    user = session.scalars(statement).first()

    if user is None:
        return None

    if not verify_password(user.password_hash, password):
        return None

    return user
