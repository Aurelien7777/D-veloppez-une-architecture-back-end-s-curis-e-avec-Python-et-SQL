"""Manage contract business logic."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.controllers.crud_controller import (
    delete_object,
    get_all,
    get_by_id,
    update_fields,
)
from epic_events.controllers.permission_controller import (
    can_create_contract,
    can_delete_contract,
    can_update_contract,
)
from epic_events.models.model import Contract, Customer, User


def get_all_contracts(session: Session) -> list[Contract]:
    """Return all contracts."""

    return get_all(session, Contract)


def get_contract_by_id(
    session: Session,
    id_contract: int,
) -> Optional[Contract]:
    """Return a contract by id."""

    return get_by_id(
        session,
        Contract,
        Contract.id_contract,
        id_contract,
    )


def get_unsigned_contracts(session: Session) -> list[Contract]:
    """Return all unsigned contracts."""

    statement = select(Contract).where(Contract.is_signed.is_(False))
    return list(session.scalars(statement).all())


def get_unpaid_contracts(session: Session) -> list[Contract]:
    """Return all contracts with remaining amount to pay."""

    statement = select(Contract).where(Contract.remaining_amount > 0)
    return list(session.scalars(statement).all())


def create_contract(
    session: Session,
    current_user: User,
    customer: Customer,
    total_amount: Decimal,
    remaining_amount: Decimal,
    is_signed: bool = False,
) -> Optional[Contract]:
    """Create a contract linked to a customer."""

    if not can_create_contract(current_user):
        return None

    contract = Contract(
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        created_at=datetime.now(),
        is_signed=is_signed,
        customer=customer,
    )

    session.add(contract)
    session.commit()

    return contract


def update_contract(
    session: Session,
    current_user: User,
    contract: Contract,
    total_amount: Optional[Decimal] = None,
    remaining_amount: Optional[Decimal] = None,
    is_signed: Optional[bool] = None,
) -> Optional[Contract]:
    """Update selected contract fields if current user is allowed."""

    if not can_update_contract(current_user, contract):
        return None

    return update_fields(
        session,
        contract,
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        is_signed=is_signed,
    )


def delete_contract(
    session: Session,
    current_user: User,
    contract: Contract,
) -> bool:
    """Delete a contract if current user is allowed."""

    if not can_delete_contract(current_user):
        return False

    return delete_object(session, contract)