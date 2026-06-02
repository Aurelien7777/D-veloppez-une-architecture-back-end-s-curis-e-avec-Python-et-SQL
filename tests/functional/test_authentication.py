from epic_events.controllers.auth_controller import authenticate_user


def test_authenticate_user_returns_user_with_valid_credentials(
    test_session,
    management_user,
):
    user = authenticate_user(
        test_session,
        "bill.bouquet@epicevents.com",
        "SecurePassword123!",
    )

    assert user is not None
    assert user.email == management_user.email
    assert user.full_name == "Bill Bouquet"


def test_authenticate_user_returns_none_with_wrong_password(
    test_session,
    management_user,
):
    user = authenticate_user(
        test_session,
        "bill.bouquet@epicevents.com",
        "WrongPassword123!",
    )

    assert user is None


def test_authenticate_user_returns_none_with_unknown_email(
    test_session,
    management_user,
):
    user = authenticate_user(
        test_session,
        "unknown@epicevents.com",
        "SecurePassword123!",
    )

    assert user is None
