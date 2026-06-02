from datetime import datetime, timedelta, timezone

import jwt
import pytest

from epic_events.controllers import token_controller


JWT_SECRET_KEY = "a" * 32
JWT_ALGORITHM = "HS256"


@pytest.fixture(autouse=True)
def token_test_config(monkeypatch, tmp_path):
    """Configure token controller for tests."""

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


def test_create_token_returns_valid_jwt(user_factory):
    user = user_factory("management", id_user=1)

    token = token_controller.create_token(user)
    payload = token_controller.decode_token(token)

    assert payload is not None
    assert payload["sub"] == "1"
    assert payload["email"] == user.email
    assert payload["role"] == "management"


def test_save_token_creates_token_file():
    token = "fake_token"

    token_controller.save_token(token)

    assert token_controller.TOKEN_FILE.exists()
    assert token_controller.TOKEN_FILE.read_text(encoding="utf-8") == token


def test_load_token_returns_saved_token():
    token = "fake_token"
    token_controller.save_token(token)

    loaded_token = token_controller.load_token()

    assert loaded_token == token


def test_load_token_returns_none_when_token_file_does_not_exist():
    loaded_token = token_controller.load_token()

    assert loaded_token is None


def test_delete_token_removes_token_file():
    token_controller.save_token("fake_token")

    token_controller.delete_token()

    assert token_controller.TOKEN_FILE.exists() is False


def test_decode_token_returns_none_with_invalid_token():
    token_controller.save_token("invalid_token")

    payload = token_controller.decode_token("invalid_token")

    assert payload is None
    assert token_controller.load_token() is None


def test_decode_token_returns_none_with_expired_token():
    expired_payload = {
        "sub": "1",
        "email": "test@test.com",
        "role": "management",
        "iat": datetime.now(tz=timezone.utc) - timedelta(hours=2),
        "exp": datetime.now(tz=timezone.utc) - timedelta(hours=1),
    }

    expired_token = jwt.encode(
        expired_payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    token_controller.save_token(expired_token)

    payload = token_controller.decode_token(expired_token)

    assert payload is None
    assert token_controller.load_token() is None