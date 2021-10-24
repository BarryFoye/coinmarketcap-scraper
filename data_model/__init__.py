"""TODO: Add description."""

# Import third-party modules
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__author__ = "Vitali Lupusor"

# Instantiate database configuration object
db_config = {
    "drivername": "postgresql",
    "username": "admin",
    "password": "test",
    "host": "localhost",
    "port": 5432,
    "database": "test",
}

# Create engine
engine = create_engine(URL.create(**db_config))
# Create session
session = sessionmaker(engine)()
# Declare database model
Base = declarative_base()
