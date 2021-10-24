"""Experimentation with SQLAlchemy table relationships."""

# Import third-party modules
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

__author__ = "Vitali Lupusor"

# Instantiate database configuration object
db_config = {
    "drivername": "postgresql",
    "username": "admin",
    "password": "test",
    "host": "localhost",
    "port": 5432,
    "database": "experiment",
}

# Create engine
engine = create_engine(URL.create(**db_config))

# Declare database model
Base = declarative_base()

association_table = Table(
    "association", Base.metadata,
    Column("left_id", ForeignKey("left.id"), primary_key=True),
    Column("right_id", ForeignKey("right.id"), primary_key=True),
)


class Parent(Base):
    __tablename__ = "left"
    id = Column(Integer, primary_key=True)
    children = relationship(
        "Child",
        secondary=association_table,
        back_populates="parents",
    )


class Child(Base):
    __tablename__ = "right"
    id = Column(Integer, primary_key=True)
    parents = relationship(
        "Parent",
        secondary=association_table,
        back_populates="children",
    )


Base.metadata.create_all(engine)
session = sessionmaker(engine)()

parent = Parent(id=1)
child_0 = Child(id=1)
child_1 = Child(id=2)
parent.children.append(child_0)
parent.children.append(child_1)

session.add(parent)
session.commit()
