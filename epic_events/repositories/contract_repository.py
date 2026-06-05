"""Contract repository."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from epic_events.models.model import Contract
from epic_events.repositories.base_repository import (
    delete_object,
    get_all,
    get_by_id,
    update_fields,
)


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


def save_contract(
    session: Session,
    contract: Contract,
) -> Contract:
    """Save a contract."""

    session.add(contract)
    session.commit()

    return contract


def update_contract_fields(
    session: Session,
    contract: Contract,
    **fields,
) -> Contract:
    """Update selected contract fields."""

    return update_fields(session, contract, **fields)


def delete_contract(
    session: Session,
    contract: Contract,
) -> bool:
    """Delete a contract."""

    return delete_object(session, contract)
