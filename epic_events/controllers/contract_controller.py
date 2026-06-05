"""Manage contract business logic."""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from epic_events.controllers.permission_controller import (
    can_create_contract,
    can_delete_contract,
    can_update_contract,
)
from epic_events.models.model import Contract, Customer, User
from epic_events.repositories import contract_repository
from epic_events.validators import validate_contract_data


def get_all_contracts(session: Session) -> list[Contract]:
    """Return all contracts."""

    return contract_repository.get_all_contracts(session)


def get_contract_by_id(
    session: Session,
    id_contract: int,
) -> Optional[Contract]:
    """Return a contract by id."""

    return contract_repository.get_contract_by_id(session, id_contract)


def get_unsigned_contracts(session: Session) -> list[Contract]:
    """Return all unsigned contracts."""

    return contract_repository.get_unsigned_contracts(session)


def get_unpaid_contracts(session: Session) -> list[Contract]:
    """Return all contracts with remaining amount to pay."""

    return contract_repository.get_unpaid_contracts(session)


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

    if not validate_contract_data(total_amount, remaining_amount):
        return None

    contract = Contract(
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        created_at=datetime.now(),
        is_signed=is_signed,
        customer=customer,
    )
    contract_repository.save_contract(session, contract)
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

    if not validate_contract_data(total_amount, remaining_amount):
        return None

    contract.update_contract_info(
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        is_signed=is_signed,
    )

    session.commit()

    return contract


def delete_contract(
    session: Session,
    current_user: User,
    contract: Contract,
) -> bool:
    """Delete a contract if current user is allowed."""

    if not can_delete_contract(current_user):
        return False

    return contract_repository.delete_contract(session, contract)
