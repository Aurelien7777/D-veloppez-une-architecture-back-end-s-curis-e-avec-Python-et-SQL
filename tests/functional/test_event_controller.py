import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from epic_events.exceptions import (
    BusinessRuleError,
    InvalidDataError,
    PermissionDeniedError,
)

from epic_events.controllers.contract_controller import create_contract
from epic_events.controllers.customer_controller import create_customer
from epic_events.controllers.event_controller import (
    assign_support_to_event,
    create_event,
    delete_event,
    get_all_events,
    get_event_by_id,
    get_events_by_support,
    get_events_without_support,
    update_event,
)


def create_test_customer(test_session, commercial_user):
    """Create a customer for event tests."""

    return create_customer(
        session=test_session,
        current_user=commercial_user,
        full_name="Kevin Casey",
        email="kevin.event@startup.io",
        phone="+67812345678",
        company_name="Cool Startup LLC",
    )


def create_test_contract(
    test_session,
    management_user,
    customer,
    is_signed=True,
):
    """Create a contract for event tests."""

    return create_contract(
        session=test_session,
        current_user=management_user,
        customer=customer,
        total_amount=Decimal("1000.00"),
        remaining_amount=Decimal("500.00"),
        is_signed=is_signed,
    )


def create_test_event(
    test_session,
    commercial_user,
    contract,
):
    """Create an event for event tests."""

    return create_event(
        session=test_session,
        current_user=commercial_user,
        contract=contract,
        name="Kevin Casey Wedding",
        start_date=datetime.now() + timedelta(days=10),
        end_date=datetime.now() + timedelta(days=11),
        location="Paris",
        attendees=100,
        notes="Wedding event notes.",
    )


def test_get_all_events_returns_events(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    events = get_all_events(test_session)

    assert event in events


def test_get_event_by_id_returns_event(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    found_event = get_event_by_id(test_session, event.id_event)

    assert found_event is not None
    assert found_event.id_event == event.id_event


def test_commercial_can_create_event_for_signed_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)

    event = create_test_event(test_session, commercial_user, contract)

    assert event is not None
    assert event.contract == contract
    assert event.name == "Kevin Casey Wedding"


def test_commercial_cannot_create_event_for_unsigned_contract(
    test_session,
    management_user,
    commercial_user,
):

    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(
        test_session,
        management_user,
        customer,
        is_signed=False,
    )

    with pytest.raises(PermissionDeniedError):
        create_test_event(test_session, commercial_user, contract)


def test_other_commercial_cannot_create_event_for_contract(
    test_session,
    management_user,
    commercial_user,
    other_commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)

    with pytest.raises(PermissionDeniedError):
        create_test_event(test_session, other_commercial_user, contract)


def test_cannot_create_two_events_for_same_contract(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)

    first_event = create_test_event(test_session, commercial_user, contract)

    with pytest.raises(BusinessRuleError):
        create_test_event(test_session, commercial_user, contract)

    assert first_event is not None


def test_management_can_assign_support_to_event(
    test_session,
    management_user,
    commercial_user,
    support_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    updated_event = assign_support_to_event(
        session=test_session,
        current_user=management_user,
        event=event,
        support_user=support_user,
    )

    assert updated_event is not None
    assert updated_event.id_support == support_user.id_user


def test_commercial_cannot_assign_support_to_event(
    test_session,
    management_user,
    commercial_user,
    support_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    with pytest.raises(PermissionDeniedError):
        assign_support_to_event(
            session=test_session,
            current_user=commercial_user,
            event=event,
            support_user=support_user,
        )

    assert event.id_support is None


def test_management_cannot_assign_non_support_user(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    with pytest.raises(InvalidDataError):
        assign_support_to_event(
            session=test_session,
            current_user=management_user,
            event=event,
            support_user=commercial_user,
        )

    assert event.id_support is None


def test_get_events_without_support_returns_unassigned_events(
    test_session,
    management_user,
    commercial_user,
    support_user,
):
    customer = create_test_customer(test_session, commercial_user)

    first_contract = create_test_contract(test_session, management_user, customer)
    second_contract = create_test_contract(test_session, management_user, customer)

    event_without_support = create_test_event(
        test_session,
        commercial_user,
        first_contract,
    )
    event_with_support = create_test_event(
        test_session,
        commercial_user,
        second_contract,
    )

    assign_support_to_event(
        session=test_session,
        current_user=management_user,
        event=event_with_support,
        support_user=support_user,
    )

    events = get_events_without_support(test_session)

    assert event_without_support in events
    assert event_with_support not in events


def test_get_events_by_support_returns_assigned_events(
    test_session,
    management_user,
    commercial_user,
    support_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    assign_support_to_event(
        session=test_session,
        current_user=management_user,
        event=event,
        support_user=support_user,
    )

    events = get_events_by_support(test_session, support_user)

    assert event in events


def test_support_can_update_assigned_event(
    test_session,
    management_user,
    commercial_user,
    support_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    assign_support_to_event(
        session=test_session,
        current_user=management_user,
        event=event,
        support_user=support_user,
    )

    updated_event = update_event(
        session=test_session,
        current_user=support_user,
        event=event,
        location="Lyon",
        attendees=120,
    )

    assert updated_event is not None
    assert updated_event.location == "Lyon"
    assert updated_event.attendees == 120


def test_support_cannot_update_unassigned_event(
    test_session,
    management_user,
    commercial_user,
    support_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    with pytest.raises(PermissionDeniedError):
        update_event(
            session=test_session,
            current_user=support_user,
            event=event,
            location="Lyon",
        )

    assert event.location == "Paris"


def test_management_can_update_any_event(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    updated_event = update_event(
        session=test_session,
        current_user=management_user,
        event=event,
        location="Marseille",
    )

    assert updated_event is not None
    assert updated_event.location == "Marseille"


def test_management_can_delete_event(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    result = delete_event(
        session=test_session,
        current_user=management_user,
        event=event,
    )

    deleted_event = get_event_by_id(test_session, event.id_event)

    assert result is True
    assert deleted_event is None


def test_commercial_cannot_delete_event(
    test_session,
    management_user,
    commercial_user,
):
    customer = create_test_customer(test_session, commercial_user)
    contract = create_test_contract(test_session, management_user, customer)
    event = create_test_event(test_session, commercial_user, contract)

    with pytest.raises(PermissionDeniedError):
        delete_event(
            session=test_session,
            current_user=commercial_user,
            event=event,
        )

    existing_event = get_event_by_id(test_session, event.id_event)

    assert existing_event is not None
