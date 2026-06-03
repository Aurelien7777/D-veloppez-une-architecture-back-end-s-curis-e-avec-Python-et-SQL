import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from epic_events.controllers.auth_controller import hash_password
from epic_events.models.model import Base, Role, User

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_session():
    """Create a temporary test database session."""

    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(engine)

    session = TestingSessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def management_role(test_session):
    """Create a management role for tests."""

    role = Role(name="management")
    test_session.add(role)
    test_session.commit()

    return role


@pytest.fixture
def management_user(test_session, management_role):
    """Create a management user for authentication tests."""

    user = User(
        full_name="Bill Bouquet",
        email="bill.bouquet@epicevents.com",
        employee_number="0711121314",
        password_hash=hash_password("SecurePassword123!"),
        role=management_role,
    )

    test_session.add(user)
    test_session.commit()

    return user


@pytest.fixture
def commercial_role(test_session):
    """Create a commercial role for tests."""

    role = Role(name="commercial")
    test_session.add(role)
    test_session.commit()

    return role


@pytest.fixture
def support_role(test_session):
    """Create a support role for tests."""

    role = Role(name="support")
    test_session.add(role)
    test_session.commit()

    return role


@pytest.fixture
def commercial_user(test_session, commercial_role):
    """Create a commercial user for tests."""

    user = User(
        full_name="Commercial User",
        email="commercial@epicevents.com",
        employee_number="COM001",
        password_hash=hash_password("SecurePassword123!"),
        role=commercial_role,
    )

    test_session.add(user)
    test_session.commit()

    return user


@pytest.fixture
def other_commercial_user(test_session, commercial_role):
    """Create another commercial user for tests."""

    user = User(
        full_name="Other Commercial User",
        email="other.commercial@epicevents.com",
        employee_number="COM002",
        password_hash=hash_password("SecurePassword123!"),
        role=commercial_role,
    )

    test_session.add(user)
    test_session.commit()

    return user


@pytest.fixture
def support_user(test_session, support_role):
    """Create a support user for tests."""

    user = User(
        full_name="Support User",
        email="support@epicevents.com",
        employee_number="SUP001",
        password_hash=hash_password("SecurePassword123!"),
        role=support_role,
    )

    test_session.add(user)
    test_session.commit()

    return user
