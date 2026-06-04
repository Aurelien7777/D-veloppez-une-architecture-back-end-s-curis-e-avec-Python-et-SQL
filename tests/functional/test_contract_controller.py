from decimal import Decimal

from epic_events.controllers.contract_controller import (
    create_contract,
    delete_contract,
    get_all_contracts,
    get_contract_by_id,
    get_unpaid_contracts,
    get_unsigned_contracts,
    update_contract,
)
from epic_events.controllers.customer_controller import create_customer


def create_test_customer(test_session, commercial_user):
    """Create a customer for contract tests."""

    return create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )


def test_get_all_contracts_returns_contracts(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    contracts = get_all_contracts(test_session)

    assert contract in contracts


def test_get_contract_by_id_returns_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    found_contract = get_contract_by_id(test_session, contract.id_contract)

    assert found_contract is not None
    assert found_contract.id_contract == contract.id_contract


def test_management_can_create_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    assert contract is not None
    assert contract.customer == customer
    assert contract.total_amount == Decimal("1000.00")


def test_commercial_cannot_create_contract(
    test_session,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=commercial_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    assert contract is None


def test_management_can_update_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    updated_contract = update_contract(
        session=test_session,
        current_user=management_user,
        contract=contract,
        remaining_amount=Decimal("0.00"),
        is_signed=True,
    )

    assert updated_contract is not None
    assert updated_contract.remaining_amount == Decimal("0.00")
    assert updated_contract.is_signed is True


def test_commercial_can_update_own_customer_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    updated_contract = update_contract(
        session=test_session,
        current_user=commercial_user,
        contract=contract,
        remaining_amount=Decimal("250.00"),
    )

    assert updated_contract is not None
    assert updated_contract.remaining_amount == Decimal("250.00")


def test_commercial_cannot_update_other_commercial_contract(
    test_session,
    management_user,
    commercial_user,
    other_commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    updated_contract = update_contract(
        session=test_session,
        current_user=other_commercial_user,
        contract=contract,
        remaining_amount=Decimal("0.00"),
    )

    assert updated_contract is None
    assert contract.remaining_amount == Decimal("500.00")


def test_support_cannot_update_contract(
    test_session,
    management_user,
    commercial_user,
    support_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    updated_contract = update_contract(
        session=test_session,
        current_user=support_user,
        contract=contract,
        is_signed=True,
    )

    assert updated_contract is None
    assert contract.is_signed is False


def test_get_unsigned_contracts_returns_only_unsigned_contracts(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    unsigned_contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("2000.00"),
        remaining_amount=Decimal("0.00"),
        is_signed=True,
    )

    unsigned_contracts = get_unsigned_contracts(test_session)

    assert unsigned_contract in unsigned_contracts
    assert all(contract.is_signed is False for contract in unsigned_contracts)


def test_get_unpaid_contracts_returns_only_unpaid_contracts(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    unpaid_contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=True,
    )

    create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("2000.00"),
        remaining_amount=Decimal("0.00"),
        is_signed=True,
    )

    unpaid_contracts = get_unpaid_contracts(test_session)

    assert unpaid_contract in unpaid_contracts
    assert all(contract.remaining_amount > 0 for contract in unpaid_contracts)


def test_management_can_delete_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    result = delete_contract(
        session=test_session,
        current_user=management_user,
        contract=contract,
    )

    deleted_contract = get_contract_by_id(test_session, contract.id_contract)

    assert result is True
    assert deleted_contract is None


def test_commercial_cannot_delete_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)

    contract = create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=False,
    )

    result = delete_contract(
        session=test_session,
        current_user=commercial_user,
        contract=contract,
    )

    existing_contract = get_contract_by_id(test_session, contract.id_contract)

    assert result is False
    assert existing_contract is not None
