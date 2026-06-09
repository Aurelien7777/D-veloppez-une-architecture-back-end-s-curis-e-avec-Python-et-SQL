"""Manage persistent authentication tokens."""

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import jwt
from dotenv import dotenv_values
from jwt import ExpiredSignatureError, InvalidTokenError
from epic_events.repositories import user_repository
from sqlalchemy.orm import Session

from epic_events.models.model import User

config = dotenv_values(".env")

TOKEN_DIRECTORY = Path.home() / ".epic_events"
TOKEN_FILE = TOKEN_DIRECTORY / "token"


def get_jwt_secret_key() -> str:
    """Return JWT secret key from environment config."""

    return config["JWT_SECRET_KEY"]


def get_jwt_algorithm() -> str:
    """Return JWT algorithm from environment config."""

    return config.get("JWT_ALGORITHM", "HS256")


def get_jwt_expiration_hours() -> int:
    """Return JWT expiration duration in hours."""

    return int(config.get("JWT_EXPIRATION_HOURS", 8))

def get_jwt_expiration_minutes() -> int:
    """Return JWT expiration duration in hours."""

    return int(config.get("JWT_EXPIRATION_MINUTES", 30))


def create_token(user: User) -> str:
    """Create a JWT for an authenticated user."""

    now = datetime.now(tz=timezone.utc)
    expiration_date = now + timedelta(minutes=get_jwt_expiration_minutes())

    payload = {
        "sub": str(user.id_user),
        "email": user.email,
        "role": user.role.name,
        "iat": now,
        "exp": expiration_date,
    }

    return jwt.encode(
        payload,
        get_jwt_secret_key(),
        algorithm=get_jwt_algorithm(),
    )


def save_token(token: str) -> None:
    """Save JWT locally."""

    TOKEN_DIRECTORY.mkdir(exist_ok=True)
    TOKEN_FILE.write_text(token, encoding="utf-8")


def load_token() -> Optional[str]:
    """Load JWT from local storage."""

    if not TOKEN_FILE.exists():
        return None

    return TOKEN_FILE.read_text(encoding="utf-8")


def delete_token() -> None:
    """Delete local JWT."""

    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT."""

    try:
        return jwt.decode(
            token,
            get_jwt_secret_key(),
            algorithms=[get_jwt_algorithm()],
        )

    except ExpiredSignatureError:
        delete_token()
        return None

    except InvalidTokenError:
        delete_token()
        return None


def get_current_user(session: Session) -> Optional[User]:
    """Return current authenticated user from local JWT."""

    token = load_token()

    if token is None:
        return None

    payload = decode_token(token)

    if payload is None:
        return None

    user_id = int(payload["sub"])

    return user_repository.get_user_by_id(session, user_id)
