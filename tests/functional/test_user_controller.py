from typing import Any

import pytest

from epic_events.exceptions import (
    BusinessRuleError,
    InvalidDataError,
    PermissionDeniedError,
)

from epic_events.controllers.auth_controller import verify_password
from epic_events.controllers.user_controller import (
    create_user as create_crm_user,
    delete_user,
    get_all_users,
    get_user_by_id,
    update_user,
)


def test_management_can_create_user_with_hashed_password(
    test_session,
    management_user,
    commercial_role,
):
    user = create_crm_user(
        session=test_session,
        current_user=management_user,
        full_name="New Commercial",
        email="new.commercial@epicevents.com",
        employee_number="COM999",
        password="SecurePassword123!",
        role=commercial_role,
    )

    assert user is not None
    assert user.email == "new.commercial@epicevents.com"
    assert user.password_hash != "SecurePassword123!"
    assert verify_password(user.password_hash, "SecurePassword123!") is True


@pytest.mark.parametrize(
    "current_user_fixture",
    [
        "commercial_user",
        "support_user",
    ],
)
def test_non_management_user_cannot_create_user(
    request: Any,
    test_session,
    current_user_fixture,
    commercial_role,
):
    current_user = request.getfixturevalue(current_user_fixture)

    with pytest.raises(PermissionDeniedError):
        create_crm_user(
            session=test_session,
            current_user=current_user,
            full_name="Blocked User",
            email="blocked@epicevents.com",
            employee_number="BLOCK001",
            password="SecurePassword123!",
            role=commercial_role,
        )


def test_get_all_users_returns_users(test_session, management_user):
    users = get_all_users(test_session)

    assert management_user in users


def test_get_user_by_id_returns_user(test_session, management_user):
    found_user = get_user_by_id(test_session, management_user.id_user)

    assert found_user is not None
    assert found_user.email == management_user.email


def test_management_can_update_user(
    test_session,
    management_user,
    commercial_user,
    support_role,
):
    updated_user = update_user(
        session=test_session,
        current_user=management_user,
        user=commercial_user,
        full_name="Updated Commercial",
        email="updated.commercial@epicevents.com",
        password="NewSecurePassword123!",
        role=support_role,
    )

    assert updated_user is not None
    assert updated_user.full_name == "Updated Commercial"
    assert updated_user.email == "updated.commercial@epicevents.com"
    assert updated_user.role.name == "support"
    assert verify_password(updated_user.password_hash, "NewSecurePassword123!") is True


def test_non_management_user_cannot_update_user(
    test_session,
    commercial_user,
    support_user,
):
    with pytest.raises(PermissionDeniedError):
        update_user(
            session=test_session,
            current_user=commercial_user,
            user=support_user,
            full_name="Blocked Update",
        )

    assert support_user.full_name == "Support User"


def test_management_can_delete_another_user(
    test_session,
    management_user,
    support_user,
):
    user_id = support_user.id_user

    result = delete_user(
        session=test_session,
        current_user=management_user,
        user=support_user,
    )

    deleted_user = get_user_by_id(test_session, user_id)

    assert result is True
    assert deleted_user is None


def test_management_cannot_delete_himself(
    test_session,
    management_user,
):
    with pytest.raises(BusinessRuleError):
        delete_user(
            session=test_session,
            current_user=management_user,
            user=management_user,
        )

    existing_user = get_user_by_id(test_session, management_user.id_user)

    assert existing_user is not None


def test_non_management_user_cannot_delete_user(
    test_session,
    commercial_user,
    support_user,
):
    with pytest.raises(PermissionDeniedError):
        delete_user(
            session=test_session,
            current_user=commercial_user,
            user=support_user,
        )

    existing_user = get_user_by_id(test_session, support_user.id_user)

    assert existing_user is not None


def test_management_cannot_create_user_with_invalid_data(
    test_session,
    management_user,
    commercial_role,
):
    with pytest.raises(InvalidDataError):
        create_crm_user(
            session=test_session,
            current_user=management_user,
            full_name="",
            email="invalid-email",
            employee_number="COM999",
            password="short",
            role=commercial_role,
        )


def test_management_cannot_update_user_with_invalid_data(
    test_session,
    management_user,
    commercial_user,
):
    with pytest.raises(InvalidDataError):
        update_user(
            session=test_session,
            current_user=management_user,
            user=commercial_user,
            email="invalid-email",
        )

    assert commercial_user.email != "invalid-email"
