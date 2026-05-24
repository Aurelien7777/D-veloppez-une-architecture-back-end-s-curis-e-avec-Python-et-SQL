import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError


load_dotenv()


def get_database_url():
    return URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
    )


def test_database_connection():
    engine = create_engine(get_database_url())

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE();"))
            database_name = result.scalar()
            print(f"Connexion réussie à la base : {database_name}")

    except SQLAlchemyError as error:
        print("Erreur de connexion à la base de données.")
        print(error)


if __name__ == "__main__":
    test_database_connection()