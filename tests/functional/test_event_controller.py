"""Functional tests for event controller."""

import pytest

from epic_events.controllers.event_controller import (
    assign_support_to_event,
    delete_event,
    get_all_events,
    get_event_by_id,
    update_event,
)
from epic_events.exceptions import (
    BusinessRuleError,
    InvalidDataError,
    PermissionDeniedError,
)


def test_get_events_returns_created_event(test_session, event_factory):
    event = event_factory()

    events = get_all_events(test_session)
    found_event = get_event_by_id(test_session, event.id_event)

    assert event in events
    assert found_event == event


def test_commercial_can_create_event_for_signed_contract(event_factory, signed_contract):
    event = event_factory()

    assert event.contract == signed_contract
    assert event.name == "Kevin Casey Wedding"


def test_commercial_cannot_create_event_for_unsigned_contract(
    event_factory,
    unsigned_contract,
):
    with pytest.raises(PermissionDeniedError):
        event_factory(contract=unsigned_contract)


def test_other_commercial_cannot_create_event_for_contract(
    event_factory,
    other_commercial_user,
):
    with pytest.raises(PermissionDeniedError):
        event_factory(current_user=other_commercial_user)


def test_cannot_create_two_events_for_same_contract(event_factory):
    first_event = event_factory()

    with pytest.raises(BusinessRuleError):
        event_factory()

    assert first_event is not None


def test_management_can_assign_support_to_event(
    test_session,
    management_user,
    support_user,
    event,
):
    updated_event = assign_support_to_event(
        session=test_session,
        current_user=management_user,
        event=event,
        support_user=support_user,
    )

    assert updated_event.id_support == support_user.id_user


def test_management_cannot_assign_same_support_twice(
    test_session,
    management_user,
    support_user,
    event_with_support,
):
    with pytest.raises(BusinessRuleError):
        assign_support_to_event(
            session=test_session,
            current_user=management_user,
            event=event_with_support,
            support_user=support_user,
        )


def test_commercial_cannot_assign_support_to_event(
    test_session,
    commercial_user,
    support_user,
    event,
):
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
    event,
):
    with pytest.raises(InvalidDataError):
        assign_support_to_event(
            session=test_session,
            current_user=management_user,
            event=event,
            support_user=commercial_user,
        )

    assert event.id_support is None


def test_support_can_update_assigned_event(
    test_session,
    support_user,
    event_with_support,
):
    updated_event = update_event(
        session=test_session,
        current_user=support_user,
        event=event_with_support,
        location="Lyon",
        attendees=120,
    )

    assert updated_event.location == "Lyon"
    assert updated_event.attendees == 120


def test_support_cannot_update_unassigned_event(
    test_session,
    support_user,
    event,
):
    with pytest.raises(PermissionDeniedError):
        update_event(
            session=test_session,
            current_user=support_user,
            event=event,
            location="Lyon",
        )

    assert event.location == "Paris"


def test_management_can_update_event_support(
    test_session,
    management_user,
    support_user,
    event,
):
    updated_event = update_event(
        session=test_session,
        current_user=management_user,
        event=event,
        support_user=support_user,
    )

    assert updated_event.id_support == support_user.id_user


def test_management_cannot_update_event_with_same_support(
    test_session,
    management_user,
    support_user,
    event_with_support,
):
    with pytest.raises(BusinessRuleError):
        update_event(
            session=test_session,
            current_user=management_user,
            event=event_with_support,
            support_user=support_user,
        )


def test_management_can_delete_event(
    test_session,
    management_user,
    event,
):
    event_id = event.id_event

    result = delete_event(
        session=test_session,
        current_user=management_user,
        event=event,
    )

    deleted_event = get_event_by_id(test_session, event_id)

    assert result is True
    assert deleted_event is None


def test_commercial_cannot_delete_event(
    test_session,
    commercial_user,
    event,
):
    with pytest.raises(PermissionDeniedError):
        delete_event(
            session=test_session,
            current_user=commercial_user,
            event=event,
        )

    existing_event = get_event_by_id(test_session, event.id_event)

    assert existing_event is not None
