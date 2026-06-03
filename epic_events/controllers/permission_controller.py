"""Manage role-based permissions."""

from epic_events.models.model import Contract, Customer, Event, User


def is_management(user: User) -> bool:
    """Return True if user belongs to management role."""

    return user.is_management()


def is_commercial(user: User) -> bool:
    """Return True if user belongs to commercial role."""

    return user.is_commercial()


def is_support(user: User) -> bool:
    """Return True if user belongs to support role."""

    return user.is_support()


def can_manage_users(user: User) -> bool:
    """Return True if user can create, update or delete users."""

    return is_management(user)


def can_create_contract(user: User) -> bool:
    """Return True if user can create contracts."""

    return is_management(user)


def can_update_contract(user: User, contract: Contract) -> bool:
    """Return True if user can update this contract."""

    if is_management(user):
        return True

    if is_commercial(user) and contract.customer.id_commercial == user.id_user:
        return True

    return False


def can_create_customer(user: User) -> bool:
    """Return True if user can create customers."""

    return is_commercial(user)


def can_update_customer(user: User, customer: Customer) -> bool:
    """Return True if user can update this customer."""

    return is_commercial(user) and customer.id_commercial == user.id_user


def can_create_event(user: User, contract: Contract) -> bool:
    """Return True if user can create an event for this contract."""

    if not is_commercial(user):
        return False

    if not contract.is_signed:
        return False

    return contract.customer.id_commercial == user.id_user


def can_assign_support_to_event(user: User) -> bool:
    """Return True if user can assign support users to events."""

    return is_management(user)


def can_update_event(user: User, event: Event) -> bool:
    """Return True if user can update this event."""

    if is_management(user):
        return True

    if is_support(user) and event.id_support == user.id_user:
        return True

    return False


def can_delete_customer(user: User) -> bool:
    """Return True if user can delete customers."""

    return is_management(user)


def can_delete_contract(user: User) -> bool:
    """Return True if user can delete contracts."""

    return user.is_management()
