from epic_events.controllers.auth_controller import hash_password, verify_password


def test_hash_password_returns_hash_different_from_plain_password():
    password = "SecurePassword123!"

    password_hash = hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$argon2id$")


def test_verify_password_returns_true_with_valid_password():
    password = "SecurePassword123!"
    password_hash = hash_password(password)

    result = verify_password(password_hash, password)

    assert result is True


def test_verify_password_returns_false_with_invalid_password():
    password = "SecurePassword123!"
    wrong_password = "WrongPassword123!"
    password_hash = hash_password(password)

    result = verify_password(password_hash, wrong_password)

    assert result is False
