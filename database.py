from sqlalchemy import create_engine
from sqlalchemy import text
from dotenv import dotenv_values
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError

config = dotenv_values(".env")


def get_database_url():
    """Create and return a URL database"""

    database_url = URL.create(
        drivername="mysql+pymysql",
        username=config["DB_USER"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=3306,
        database=config["DB_NAME"],
    )
    return database_url


engine = create_engine(get_database_url())


def test_connection_database():
    """Test connection with data base

    Create "engine" that takes database URL argument
    Execute method "engine.connect" transformed to connection
    "result" contains connection.execute that execute query SQL
    """

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES;"))
            print("Connection successful")
            print(result.all())

    except SQLAlchemyError as error:
        print("Erreur de connexion à la base de données.")
        print(error)


if __name__ == "__main__":
    test_connection_database()
