from datetime import datetime, timedelta, timezone

import jwt
import pytest

from epic_events.controllers import token_controller


JWT_SECRET_KEY = "a" * 32
JWT_ALGORITHM = "HS256"


@pytest.fixture(autouse=True)
def token_test_config(monkeypatch, tmp_path):
    """Configure token controller for functional tests."""

    token_directory = tmp_path / ".epic_events"
    token_file = token_directory / "token"

    monkeypatch.setattr(token_controller, "TOKEN_DIRECTORY", token_directory)
    monkeypatch.setattr(token_controller, "TOKEN_FILE", token_file)
    monkeypatch.setattr(
        token_controller,
        "get_jwt_secret_key",
        lambda: JWT_SECRET_KEY,
    )
    monkeypatch.setattr(
        token_controller,
        "get_jwt_algorithm",
        lambda: JWT_ALGORITHM,
    )
    monkeypatch.setattr(
        token_controller,
        "get_jwt_expiration_hours",
        lambda: 8,
    )


def test_get_current_user_returns_user_with_valid_token(
    test_session,
    management_user,
):
    token = token_controller.create_token(management_user)
    token_controller.save_token(token)

    current_user = token_controller.get_current_user(test_session)

    assert current_user is not None
    assert current_user.id_user == management_user.id_user
    assert current_user.email == management_user.email
    assert current_user.role.name == "management"


def test_get_current_user_returns_none_without_token(test_session):
    current_user = token_controller.get_current_user(test_session)

    assert current_user is None


def test_get_current_user_returns_none_with_invalid_token(test_session):
    token_controller.save_token("invalid_token")

    current_user = token_controller.get_current_user(test_session)

    assert current_user is None
    assert token_controller.load_token() is None


def test_get_current_user_returns_none_when_user_does_not_exist(test_session):
    payload = {
        "sub": "999",
        "email": "unknown@test.com",
        "role": "management",
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    token_controller.save_token(token)

    current_user = token_controller.get_current_user(test_session)

    assert current_user is None


def test_get_current_user_returns_none_with_expired_token(test_session):
    payload = {
        "sub": "1",
        "email": "bill.bouquet@epicevents.com",
        "role": "management",
        "iat": datetime.now(tz=timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(tz=timezone.utc) - timedelta(hours=1),
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    token_controller.save_token(token)

    current_user = token_controller.get_current_user(test_session)

    assert current_user is None
    assert token_controller.load_token() is None