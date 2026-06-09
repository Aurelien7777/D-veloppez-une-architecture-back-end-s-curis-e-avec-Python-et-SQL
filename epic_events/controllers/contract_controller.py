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
from epic_events.exceptions import InvalidDataError, PermissionDeniedError
from epic_events.monitoring import log_contract_signed


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
) -> Contract:
    """Create a contract linked to a customer."""

    if not can_create_contract(current_user):
        raise PermissionDeniedError("Seul un membre de la gestion peut créer un contrat")

    if not validate_contract_data(total_amount, remaining_amount):
        raise InvalidDataError("Les données du contrat sont invalides.")

    contract = Contract(
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        created_at=datetime.now(),
        is_signed=is_signed,
        customer=customer,
    )
    contract_repository.save_contract(session, contract)
    session.commit()

    if contract.is_signed:
        log_contract_signed(
            contract_id=contract.id_contract,
            current_user_id=current_user.id_user,
        )

    return contract


def update_contract(
    session: Session,
    current_user: User,
    contract: Contract,
    total_amount: Optional[Decimal] = None,
    remaining_amount: Optional[Decimal] = None,
    is_signed: Optional[bool] = None,
) -> Contract:
    """Update selected contract fields if current user is allowed."""

    if not can_update_contract(current_user, contract):
        raise PermissionDeniedError("Vous n'êtes pas autorisé à modifier ce contrat.")

    new_total_amount = total_amount if total_amount is not None else contract.total_amount
    new_remaining_amount = (
        remaining_amount if remaining_amount is not None else contract.remaining_amount
    )

    if not validate_contract_data(new_total_amount, new_remaining_amount):
        raise InvalidDataError("Les données du contrat sont invalides.")

    was_unsigned = not contract.is_signed

    contract.update_contract_info(
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        is_signed=is_signed,
    )

    session.commit()

    if was_unsigned and contract.is_signed:
        log_contract_signed(
            contract_id=contract.id_contract,
            current_user_id=current_user.id_user,
        )

    return contract


def delete_contract(
    session: Session,
    current_user: User,
    contract: Contract,
) -> bool:
    """Delete a contract if current user is allowed."""

    if not can_delete_contract(current_user):
        raise PermissionDeniedError("Vous n'êtes pas autorisé à supprimer ce contrat.")

    deleted = contract_repository.delete_contract(session, contract)
    session.commit()

    return deleted
