"""Data model."""

# Import third-party modules
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import (
    BIGINT, DateTime, Float, Integer, LargeBinary, String, VARCHAR
)

# Import local modules
from . import Base

__author__ = "Vitali Lupusor"


class Coin(Base):
    """Coin reference table."""

    __tablename__ = "coin"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(
        String, nullable=False, unique=False, comment="Currency name",
    )
    symbol = Column(
        VARCHAR(25), nullable=False, unique=False, comment="Currency symbol",
    )
    slug = Column(VARCHAR(50), nullable=False, unique=True, comment="")
    max_supply = Column(BIGINT, comment="")
    date_added = Column(DateTime, comment="Date when added to the market")
    market = relationship("Market")
    quotes = relationship("Quote")
    tags = relationship("Tag")


class Market(Base):
    """Market table."""

    __tablename__ = "market_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(
        Integer, ForeignKey("coin.id"), index=True, nullable=False,
        comment="Foreign key for the 'coin' table",
    )
    num_market_pairs = Column(Integer, comment="")
    circulating_supply = Column(Float, comment="")
    total_supply = Column(Float, comment="")
    cmc_rank = Column(Integer, comment="")
    last_updated = Column(DateTime, comment="")
    coins = relationship(
        "Coin",
        back_populates="market",
        collection_class=set,
    )


class Platform(Base):
    """Platform table."""

    __tablename__ = "platform"

    id = Column(Integer, primary_key=True, autoincrement=False)
    platform_id = Column(Integer, index=True, nullable=False)
    token_address = Column(LargeBinary, unique=True, comment="")


class Quote(Base):
    """Quotes table."""

    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(
        Integer, ForeignKey("coin.id"), index=True, nullable=False,
    )
    currency = Column(
        VARCHAR(10), nullable=False, comment="Name of the currency",
    )
    price = Column(Float, nullable=False, comment="")
    vol_24 = Column(Float, comment="")
    pct_change_1h = Column(Float, comment="")
    pct_change_24h = Column(Float, comment="")
    pct_change_7d = Column(Float, comment="")
    market_cap = Column(Float, comment="")
    fully_diluted_mc = Column(Float, comment="")
    last_updated = Column(DateTime, nullable=False, comment="")
    coins = relationship(
        "Coin",
        back_populates="quotes",
        collection_class=set,
        foreign_keys=[coin_id],
    )


class Tag(Base):
    """Tag table."""

    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(
        Integer, ForeignKey("coin.id"), index=True, nullable=False,
        comment="Foreign key for 'coin' table",
    )
    tag_id = Column(
        Integer, ForeignKey("tag_ref.id"), index=True, nullable=False,
        comment="Foreign key for 'tag_ref' table",
    )
    coins = relationship(
        "Coin",
        back_populates="tags",
        collection_class=set,
        foreign_keys=[coin_id],
    )
    tags = relationship(
        "TagReference",
        back_populates="tags",
        collection_class=set,
        foreign_keys=[tag_id],
    )


class TagReference(Base):
    """Tag reference table."""

    __tablename__ = "tag_ref"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False, unique=True, comment="Tag name")
    tags = relationship("Tag")
