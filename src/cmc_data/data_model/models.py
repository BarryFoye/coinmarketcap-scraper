"""Data model."""

# Import third-party modules
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import (
    BIGINT, DateTime, Float, Integer, LargeBinary, String,
)

# Import local modules
from . import Base

__author__ = "Vitali Lupusor"


coin_tag = Table(
    "coin_tag",
    Base.metadata,
    Column("market_id", ForeignKey("market.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class Coin(Base):
    """Coin reference table."""

    __tablename__ = "coin"

    id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    name = Column(
        String, nullable=False, unique=False, comment="Currency name",
    )
    symbol = Column(
        String, nullable=False, unique=False, comment="Currency symbol",
    )
    slug = Column(String, nullable=False, unique=True, comment="")
    max_supply = Column(BIGINT, comment="")
    date_added = Column(
        DateTime, nullable=False, comment="Date when added to the market",
    )
    market = relationship("Market")


class Market(Base):
    """Market table."""

    __tablename__ = "market"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    coin_id = Column(
        Integer, ForeignKey("coin.id"), index=True, nullable=False,
        comment="Foreign key for the 'coin' table",
    )
    platform_id = Column(
        Integer, ForeignKey("platform.id"), index=True,
        comment="Foreign key for the 'platform' table",
    )
    num_market_pairs = Column(Integer, comment="")
    circulating_supply = Column(Float, comment="")
    total_supply = Column(Float, comment="")
    cmc_rank = Column(Integer, comment="")
    last_updated = Column(DateTime, comment="")
    tags = relationship(
        "Tag",
        secondary=coin_tag,
        back_populates="market",
        collection_class=set,
    )
    platforms = relationship(
        "Platform",
        back_populates="market",
        collection_class=set,
    )
    quotes = relationship(
        "Quote",
        back_populates="market",
        collection_class=set,
    )
    coins = relationship(
        "Coin",
        back_populates="market",
        collection_class=set,
    )


class TagReference(Base):
    """Tag reference table."""

    __tablename__ = "tag_ref"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, comment="Tag name")
    tags = relationship("Tag")


class Tag(Base):
    """Tag table."""

    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tag_id = Column(
        Integer, ForeignKey("tag_ref.id"), index=True, nullable=False,
        comment="Foreign key for 'tag_ref' table",
    )
    market = relationship(
        "Market",
        secondary=coin_tag,
    )
    tags = relationship(
        "TagReference",
        back_populates="tags",
    )


class Platform(Base):
    """Platform table."""

    __tablename__ = "platform"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    coin_id = Column(
        Integer, ForeignKey("coin.id"), index=True, nullable=False,
    )
    token_address = Column(
        LargeBinary, nullable=False, unique=True,
        comment="Unique token address",
    )
    coins = relationship("Coin")
    market = relationship("Market")


class Quote(Base):
    """Quotes table."""

    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    market_id = Column(
        Integer, ForeignKey("market.id"), index=True, nullable=False,
    )
    currency = Column(String, nullable=False, comment="Name of the currency")
    price = Column(Float, nullable=False, comment="")
    vol_24 = Column(Float, comment="")
    pct_change_1h = Column(Float, comment="")
    pct_change_24h = Column(Float, comment="")
    pct_change_7d = Column(Float, comment="")
    market_cap = Column(Float, comment="")
    fully_diluted_mc = Column(Float, comment="")
    last_updated = Column(DateTime, nullable=False, comment="")
    market = relationship(
        "Market",
        back_populates="quotes",
    )
