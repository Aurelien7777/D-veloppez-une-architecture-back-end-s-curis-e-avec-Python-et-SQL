import pytest
from epic_events.controllers.customer_controller import (
    create_customer,
    delete_customer,
    get_all_customers,
    get_customer_by_id,
    update_customer,
)

from epic_events.exceptions import PermissionDeniedError


def test_get_all_customers_returns_customers(
    test_session,
    commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    customers = get_all_customers(test_session)

    assert customer in customers


def test_get_customer_by_id_returns_customer(
    test_session,
    commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    found_customer = get_customer_by_id(test_session, customer.id_customer)

    assert found_customer is not None
    assert found_customer.email == "kevin@startup.io"


def test_create_customer_with_commercial_user(
    test_session,
    commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    assert customer is not None
    assert customer.full_name == "Kevin Casey"
    assert customer.id_commercial == commercial_user.id_user


def test_create_customer_with_support_user_returns_none(
    test_session,
    support_user,
):
    with pytest.raises(PermissionDeniedError):
        create_customer(
            session=test_session,
            current_user=support_user,
            full_name="Kevin Casey",
            email="kevin@startup.io",
            phone="+67812345678",
            company_name="Cool Startup LLC",
        )


def test_update_customer_can_update_one_field(
    test_session,
    commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    updated_customer = update_customer(
        session=test_session,
        current_user=commercial_user,
        customer=customer,
        phone="+33600000000",
    )

    assert updated_customer is not None
    assert updated_customer.phone == "+33600000000"
    assert updated_customer.email == "kevin@startup.io"


def test_update_customer_can_update_multiple_fields(
    test_session,
    commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    updated_customer = update_customer(
        session=test_session,
        current_user=commercial_user,
        customer=customer,
        email="new.kevin@startup.io",
        company_name="New Startup LLC",
    )

    assert updated_customer is not None
    assert updated_customer.email == "new.kevin@startup.io"
    assert updated_customer.company_name == "New Startup LLC"
    assert updated_customer.phone == "+67812345678"


def test_other_commercial_cannot_update_customer(
    test_session,
    commercial_user,
    other_commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    updated_customer = update_customer(
        session=test_session,
        current_user=other_commercial_user,
        customer=customer,
        phone="+33600000000",
    )

    assert updated_customer is None
    assert customer.phone == "+67812345678"


def test_management_can_delete_customer(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    result = delete_customer(
        session=test_session,
        current_user=management_user,
        customer=customer,
    )

    deleted_customer = get_customer_by_id(test_session, customer.id_customer)

    assert result is True
    assert deleted_customer is None


def test_commercial_cannot_delete_customer(
    test_session,
    commercial_user,
):
    customer = create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )

    result = delete_customer(
        session=test_session,
        current_user=commercial_user,
        customer=customer,
    )

    existing_customer = get_customer_by_id(test_session, customer.id_customer)

    assert result is False
    assert existing_customer is not None
