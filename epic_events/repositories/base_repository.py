"""Generic CRUD helpers."""

from typing import Any, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


def get_all(session: Session, model: type[ModelType]) -> list[ModelType]:
    """Return all objects for a model."""

    statement = select(model)
    return list(session.scalars(statement).all())


def get_by_id(
    session: Session,
    model: type[ModelType],
    id_field: Any,
    id_value: int,
) -> Optional[ModelType]:
    """Return one object by id."""

    statement = select(model).where(id_field == id_value)
    return session.scalars(statement).first()


def delete_object(
    session: Session,
    obj: ModelType,
) -> bool:
    """Delete an object."""

    session.delete(obj)
    session.commit()

    return True
