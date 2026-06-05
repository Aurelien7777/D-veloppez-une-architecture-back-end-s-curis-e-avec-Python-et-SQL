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

    def update_profile(
        self,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        employee_number: Optional[str] = None,
        password_hash: Optional[str] = None,
        role: Optional["Role"] = None,
    ) -> None:
        """Update user profile information."""

        if full_name is not None:
            self.full_name = full_name

        if email is not None:
            self.email = email

        if employee_number is not None:
            self.employee_number = employee_number

        if password_hash is not None:
            self.password_hash = password_hash

        if role is not None:
            self.role = role


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

    def update_contact_info(
        self,
        full_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company_name: Optional[str] = None,
    ) -> None:
        """Update customer contact information."""

        if full_name is not None:
            self.full_name = full_name

        if email is not None:
            self.email = email

        if phone is not None:
            self.phone = phone

        if company_name is not None:
            self.company_name = company_name

        self.updated_at = datetime.now()


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

    def update_amounts(
        self,
        total_amount: Optional[Decimal] = None,
        remaining_amount: Optional[Decimal] = None,
    ) -> None:
        """Update contract amounts."""

        if total_amount is not None:
            self.total_amount = total_amount

        if remaining_amount is not None:
            self.remaining_amount = remaining_amount

    def update_signature_status(self, is_signed: Optional[bool] = None) -> None:
        """Update contract signature status."""

        if is_signed is not None:
            self.is_signed = is_signed

    def update_contract_info(
        self,
        total_amount: Optional[Decimal] = None,
        remaining_amount: Optional[Decimal] = None,
        is_signed: Optional[bool] = None,
    ) -> None:
        """Update contract information."""

        self.update_amounts(
            total_amount=total_amount,
            remaining_amount=remaining_amount,
        )
        self.update_signature_status(is_signed)


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

    def assign_support(self, support_user: User) -> None:
        """Assign a support user to the event."""

        if not support_user.is_support():
            raise ValueError("Assigned user must belong to support role.")

        self.support = support_user

    def update_event_info(
        self,
        name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        location: Optional[str] = None,
        attendees: Optional[int] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Update event information."""

        if name is not None:
            self.name = name

        if start_date is not None:
            self.start_date = start_date

        if end_date is not None:
            self.end_date = end_date

        if location is not None:
            self.location = location

        if attendees is not None:
            self.attendees = attendees

        if notes is not None:
            self.notes = notes
