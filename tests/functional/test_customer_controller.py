"""Functional tests for customer controller."""

import pytest

from epic_events.controllers.customer_controller import (
    create_customer,
    delete_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer,
)
from epic_events.exceptions import PermissionDeniedError

CUSTOMER_DATA = {
    "full_name": "Kevin Casey",
    "email": "kevin@startup.io",
    "phone": "0678123456",
    "company_name": "Cool Startup LLC",
}


def create_test_customer(test_session, commercial_user, **overrides):
    """Create a customer for customer controller tests."""

    customer_data = CUSTOMER_DATA | overrides

    return create_customer(
        session=test_session,
        current_user=commercial_user,
        **customer_data,
    )


def test_get_customer_queries_return_created_customer(
    test_session,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    customers = get_all_customers(test_session)
    found_customer = get_customer_by_id(test_session, customer.id_customer)

    assert customer in customers
    assert found_customer is not None
    assert found_customer.email == CUSTOMER_DATA["email"]


def test_commercial_can_create_customer(
    test_session,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    assert customer.full_name == CUSTOMER_DATA["full_name"]
    assert customer.id_commercial == commercial_user.id_user


@pytest.mark.parametrize(
    "user_fixture",
    [
        "support_user",
        "management_user",
    ],
)
def test_non_commercial_users_cannot_create_customer(
    request,
    test_session,
    user_fixture,
):
    current_user = request.getfixturevalue(user_fixture)

    with pytest.raises(PermissionDeniedError):
        create_customer(
            session=test_session,
            current_user=current_user,
            **CUSTOMER_DATA,
        )


@pytest.mark.parametrize(
    "update_data, expected_values",
    [
        (
            {"phone": "0600000000"},
            {
                "phone": "0600000000",
                "email": CUSTOMER_DATA["email"],
                "company_name": CUSTOMER_DATA["company_name"],
            },
        ),
        (
            {
                "email": "new.kevin@startup.io",
                "company_name": "New Startup LLC",
            },
            {
                "phone": CUSTOMER_DATA["phone"],
                "email": "new.kevin@startup.io",
                "company_name": "New Startup LLC",
            },
        ),
    ],
)
def test_commercial_can_update_customer(
    test_session,
    commercial_user,
    update_data,
    expected_values,
):
    customer = create_test_customer(test_session, commercial_user)

    updated_customer = update_customer(
        session=test_session,
        current_user=commercial_user,
        customer=customer,
        **update_data,
    )

    assert updated_customer.phone == expected_values["phone"]
    assert updated_customer.email == expected_values["email"]
    assert updated_customer.company_name == expected_values["company_name"]


@pytest.mark.parametrize(
    "user_fixture",
    [
        "other_commercial_user",
        "support_user",
        "management_user",
    ],
)
def test_unauthorized_users_cannot_update_customer(
    request,
    test_session,
    commercial_user,
    user_fixture,
):
    customer = create_test_customer(test_session, commercial_user)
    current_user = request.getfixturevalue(user_fixture)

    with pytest.raises(PermissionDeniedError):
        update_customer(
            session=test_session,
            current_user=current_user,
            customer=customer,
            phone="0640302010",
        )


def test_management_can_delete_customer(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    customer_id = customer.id_customer

    result = delete_customer(
        session=test_session,
        current_user=management_user,
        customer=customer,
    )

    deleted_customer = get_customer_by_id(test_session, customer_id)

    assert result is True
    assert deleted_customer is None


@pytest.mark.parametrize(
    "user_fixture",
    [
        "commercial_user",
        "support_user",
    ],
)
def test_non_management_users_cannot_delete_customer(
    request,
    test_session,
    commercial_user,
    user_fixture,
):
    customer = create_test_customer(test_session, commercial_user)
    current_user = request.getfixturevalue(user_fixture)

    with pytest.raises(PermissionDeniedError):
        delete_customer(
            session=test_session,
            current_user=current_user,
            customer=customer,
        )
