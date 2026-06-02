from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    pass


class User(Base):
    """Represent an Epic Events employee.

    A user can belong to one of the company departments:
    commercial, support, or management. Users are authenticated
    employees who can access the CRM according to their role.
    """

    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    employee_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    id_role: Mapped[int] = mapped_column(
        ForeignKey("roles.id_role"),
        nullable=False,
    )

    role: Mapped["Role"] = relationship(back_populates="users")
    customers: Mapped[List["Customer"]] = relationship(back_populates="commercial")
    events: Mapped[List["Event"]] = relationship(back_populates="support")

    def __repr__(self) -> str:
        return (
            f"User(id_user={self.id_user!r}, "
            f"full_name={self.full_name!r}, "
            f"role={self.role!r})"
        )
    
    def is_management(self) -> bool:
        """Return True if user belongs to management role."""

        return self.role.name == "management"

    def is_commercial(self) -> bool:
        """Return True if user belongs to commercial role."""

        return self.role.name == "commercial"

    def is_support(self) -> bool:
        """Return True if user belongs to support role."""

        return self.role.name == "support"


class Role(Base):
    """Represent an employee role in the CRM.

    A role defines the department of an employee and is used
    to determine which actions the user is allowed to perform.
    """

    __tablename__ = "roles"

    id_role: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship(back_populates="role")


class Customer(Base):
    """Represent a customer managed by Epic Events.

    A customer is linked to a commercial employee and contains
    contact information used to manage contracts and events.
    """

    __tablename__ = "customers"

    id_customer: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    id_commercial: Mapped[int] = mapped_column(
        ForeignKey("users.id_user"),
        nullable=False,
    )

    commercial: Mapped["User"] = relationship(back_populates="customers")
    contracts: Mapped[List["Contract"]] = relationship(back_populates="customer")


class Contract(Base):
    """Represent a contract between Epic Events and a customer.

    A contract is linked to a customer. The commercial contact
    for the contract is the commercial employee assigned to the customer.
    """

    __tablename__ = "contracts"

    id_contract: Mapped[int] = mapped_column(primary_key=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    remaining_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_signed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    id_customer: Mapped[int] = mapped_column(
        ForeignKey("customers.id_customer"),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(back_populates="contracts")
    event: Mapped[Optional["Event"]] = relationship(back_populates="contract")


class Event(Base):
    """Represent an event organized by Epic Events.

    An event is linked to a signed contract and can be assigned
    to a support employee responsible for its organization.
    """

    __tablename__ = "events"

    id_event: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    attendees: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    id_contract: Mapped[int] = mapped_column(
        ForeignKey("contracts.id_contract"),
        nullable=False,
        unique=True,
    )
    id_support: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id_user"),
        nullable=True,
    )

    contract: Mapped["Contract"] = relationship(back_populates="event")
    support: Mapped[Optional["User"]] = relationship(back_populates="events")
