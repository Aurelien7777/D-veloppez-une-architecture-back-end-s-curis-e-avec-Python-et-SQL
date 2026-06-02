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
