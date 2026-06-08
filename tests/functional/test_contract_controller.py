"""Functional tests for contract controller."""

from decimal import Decimal

import pytest

from epic_events.controllers.contract_controller import (
    delete_contract,
    get_all_contracts,
    get_contract_by_id,
    get_unpaid_contracts,
    get_unsigned_contracts,
    update_contract,
)
from epic_events.exceptions import PermissionDeniedError


def test_get_all_contracts_returns_contracts(test_session, contract_factory):
    contract = contract_factory()

    contracts = get_all_contracts(test_session)

    assert contract in contracts


def test_get_contract_by_id_returns_contract(test_session, contract_factory):
    contract = contract_factory()

    found_contract = get_contract_by_id(test_session, contract.id_contract)

    assert found_contract is not None
    assert found_contract.id_contract == contract.id_contract


def test_commercial_cannot_create_contract(contract_factory, commercial_user):
    with pytest.raises(PermissionDeniedError):
        contract_factory(current_user=commercial_user)


def test_management_can_update_contract(
    test_session,
    management_user,
    contract_factory,
):
    contract = contract_factory()

    updated_contract = update_contract(
        session=test_session,
        current_user=management_user,
        contract=contract,
        remaining_amount=Decimal("0.00"),
        is_signed=True,
    )

    assert updated_contract.remaining_amount == Decimal("0.00")
    assert updated_contract.is_signed is True


def test_commercial_can_update_own_customer_contract(
    test_session,
    commercial_user,
    contract_factory,
):
    contract = contract_factory()

    updated_contract = update_contract(
        session=test_session,
        current_user=commercial_user,
        contract=contract,
        remaining_amount=Decimal("250.00"),
    )

    assert updated_contract.remaining_amount == Decimal("250.00")


@pytest.mark.parametrize(
    "user_fixture",
    [
        "other_commercial_user",
        "support_user",
    ],
)
def test_unauthorized_users_cannot_update_contract(
    request,
    test_session,
    user_fixture,
    contract_factory,
):
    current_user = request.getfixturevalue(user_fixture)
    contract = contract_factory()

    with pytest.raises(PermissionDeniedError):
        update_contract(
            session=test_session,
            current_user=current_user,
            contract=contract,
            remaining_amount=Decimal("0.00"),
        )


def test_get_unsigned_contracts_returns_only_unsigned_contracts(
    test_session,
    contract_factory,
):
    unsigned_contract = contract_factory(is_signed=False)
    contract_factory(
        total_amount=Decimal("2000.00"),
        remaining_amount=Decimal("0.00"),
        is_signed=True,
    )

    unsigned_contracts = get_unsigned_contracts(test_session)

    assert unsigned_contract in unsigned_contracts
    assert all(contract.is_signed is False for contract in unsigned_contracts)


def test_get_unpaid_contracts_returns_only_unpaid_contracts(
    test_session,
    contract_factory,
):
    unpaid_contract = contract_factory(is_signed=True)
    contract_factory(
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
    contract_factory,
):
    contract = contract_factory()
    contract_id = contract.id_contract

    result = delete_contract(
        session=test_session,
        current_user=management_user,
        contract=contract,
    )

    deleted_contract = get_contract_by_id(test_session, contract_id)

    assert result is True
    assert deleted_contract is None


def test_commercial_cannot_delete_contract(
    test_session,
    commercial_user,
    contract_factory,
):
    contract = contract_factory()

    with pytest.raises(PermissionDeniedError):
        delete_contract(
            session=test_session,
            current_user=commercial_user,
            contract=contract,
        )