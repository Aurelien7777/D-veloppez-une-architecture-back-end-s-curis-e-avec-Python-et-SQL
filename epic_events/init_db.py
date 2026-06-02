"""Create database tables from SQLAlchemy models."""

from epic_events.database import engine
from epic_events.models.model import Base


def init_database():
    """Create all tables defined in SQLAlchemy models."""

    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_database()
