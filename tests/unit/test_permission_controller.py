from epic_events.controllers.permission_controller import (
    can_assign_support_to_event,
    can_create_contract,
    can_create_customer,
    can_create_event,
    can_manage_users,
    can_update_contract,
    can_delete_contract,
    can_update_customer,
    can_update_event,
    is_commercial,
    is_management,
    is_support,
)


def test_user_role_checks(user_factory):
    management_user = user_factory("management")
    commercial_user = user_factory("commercial")
    support_user = user_factory("support")

    assert is_management(management_user) is True
    assert is_commercial(commercial_user) is True
    assert is_support(support_user) is True


def test_management_can_manage_users_create_contracts_and_assign_support(
    user_factory,
):
    management_user = user_factory("management")

    assert can_manage_users(management_user) is True
    assert can_create_contract(management_user) is True
    assert can_assign_support_to_event(management_user) is True


def test_commercial_can_create_customer(user_factory):
    commercial_user = user_factory("commercial")

    assert can_create_customer(commercial_user) is True


def test_support_cannot_create_customer_or_contract(user_factory):
    support_user = user_factory("support")

    assert can_create_customer(support_user) is False
    assert can_create_contract(support_user) is False


def test_commercial_can_update_own_customer(
    user_factory,
    customer_factory,
):
    commercial_user = user_factory("commercial", id_user=1)
    customer = customer_factory(id_commercial=1)

    assert can_update_customer(commercial_user, customer) is True


def test_commercial_cannot_update_other_commercial_customer(
    user_factory,
    customer_factory,
):
    commercial_user = user_factory("commercial", id_user=1)
    customer = customer_factory(id_commercial=2)

    assert can_update_customer(commercial_user, customer) is False


def test_management_can_update_any_contract(
    user_factory,
    customer_factory,
    contract_factory,
):
    management_user = user_factory("management", id_user=1)
    customer = customer_factory(id_commercial=2)
    contract = contract_factory(customer)

    assert can_update_contract(management_user, contract) is True


def test_commercial_can_update_own_customer_contract(
    user_factory,
    customer_factory,
    contract_factory,
):
    commercial_user = user_factory("commercial", id_user=1)
    customer = customer_factory(id_commercial=1)
    contract = contract_factory(customer)

    assert can_update_contract(commercial_user, contract) is True


def test_commercial_cannot_update_other_commercial_contract(
    user_factory,
    customer_factory,
    contract_factory,
):
    commercial_user = user_factory("commercial", id_user=1)
    customer = customer_factory(id_commercial=2)
    contract = contract_factory(customer)

    assert can_update_contract(commercial_user, contract) is False


def test_commercial_can_create_event_for_signed_contract_of_own_customer(
    user_factory,
    customer_factory,
    contract_factory,
):
    commercial_user = user_factory("commercial", id_user=1)
    customer = customer_factory(id_commercial=1)
    contract = contract_factory(customer, is_signed=True)

    assert can_create_event(commercial_user, contract) is True


def test_commercial_cannot_create_event_for_unsigned_contract(
    user_factory,
    customer_factory,
    contract_factory,
):
    commercial_user = user_factory("commercial", id_user=1)
    customer = customer_factory(id_commercial=1)
    contract = contract_factory(customer, is_signed=False)

    assert can_create_event(commercial_user, contract) is False


def test_commercial_cannot_create_event_for_other_commercial_customer(
    user_factory,
    customer_factory,
    contract_factory,
):
    commercial_user = user_factory("commercial", id_user=1)
    customer = customer_factory(id_commercial=2)
    contract = contract_factory(customer, is_signed=True)

    assert can_create_event(commercial_user, contract) is False


def test_support_can_update_assigned_event(
    user_factory,
    event_factory,
):
    support_user = user_factory("support", id_user=3)
    event = event_factory(id_support=3)

    assert can_update_event(support_user, event) is True


def test_support_cannot_update_unassigned_event(
    user_factory,
    event_factory,
):
    support_user = user_factory("support", id_user=3)
    event = event_factory(id_support=4)

    assert can_update_event(support_user, event) is False


def test_management_can_update_any_event(
    user_factory,
    event_factory,
):
    management_user = user_factory("management", id_user=1)
    event = event_factory(id_support=4)

    assert can_update_event(management_user, event) is True


def test_management_can_delete_contract(user_factory):
    management_user = user_factory("management")

    assert can_delete_contract(management_user) is True


def test_commercial_cannot_delete_contract(user_factory):
    commercial_user = user_factory("commercial")

    assert can_delete_contract(commercial_user) is False
