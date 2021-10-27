"""Data model for Coinmarketcap data."""

# Import standard modules
from os import getenv, path

# Import third-party modules
from dotenv import load_dotenv

# Import third-party modules
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__author__ = "Vitali Lupusor"

# Load environment variables from the `.env` file
load_dotenv(path.join(next(iter(__path__)), ".env"))  # type: ignore
del load_dotenv, path  # Clean up

# Instantiate database configuration object
db_config = {
    "drivername": getenv("DB_DRIVER") or "postgresql",
    "username": getenv("DB_USER") or "admin",
    "password": getenv("DB_PASSWORD") or "admin",
    "host": getenv("DB_HOST") or "localhost",
    "port": getenv("DB_PORT") or 5432,
    "database": getenv("DB_NAME") or "test",
}

# Create engine
engine = create_engine(URL.create(**db_config))
# Create session
session = sessionmaker(engine)()
# Declare database model
Base = declarative_base()
