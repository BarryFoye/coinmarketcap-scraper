# Import standard modules
import datetime
import json
import logging
from random import randint
from time import sleep
from typing import Any, Dict, List, Optional

# Import third-party modules
import click
import requests
from bs4 import BeautifulSoup
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import (
    BIGINT, DateTime, Float, Integer, LargeBinary, String,
)
from sqlalchemy_utils import create_database, database_exists


def get_proxies() -> Optional[List[dict]]:
    """
    Scrape proxy server information from https://www.sslproxies.org.

    Returns
    -------
        List[dict]
            List of proxy servers.

        NoneType
            If failed to retrieve a response from the website.
    """
    # Declare variables
    url = "https://www.sslproxies.org"

    # Request proxies
    payload = requests.get(url)

    # Validate response
    content = b""
    if payload.ok:
        content = payload.content

    # Parse HTML
    soup = None
    if content:
        soup = BeautifulSoup(content, "html.parser")

    if soup:
        header = [
            value.text for value in soup.table.thead.tr.findAll("th")
        ]
        body = [
            [tag.text for tag in value.findAll("td")]
            for value in soup.table.tbody.findAll("tr")
        ]

        return [dict(zip(header, row)) for row in body]

    return None


# Import third-party modules

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
    name = Column(String, nullable=False, unique=False)
    symbol = Column(String, nullable=False, unique=False)
    slug = Column(String, nullable=False, unique=True)
    market = relationship("Market")


class Market(Base):
    """Market table."""

    __tablename__ = "market"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    coin_id = Column(
        Integer, ForeignKey("coin.id"), index=True, nullable=False,
    )
    platform_id = Column(
        Integer, ForeignKey("platform.id"), index=True,
    )
    num_market_pairs = Column(Integer)
    date_added = Column(DateTime, nullable=False)
    max_supply = Column(BIGINT)
    circulating_supply = Column(Float)
    total_supply = Column(Float)
    cmc_rank = Column(Integer)
    last_updated = Column(DateTime)
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
    name = Column(String, nullable=False, unique=True)
    tags = relationship("Tag")


class Tag(Base):
    """Tag table."""

    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tag_id = Column(
        Integer, ForeignKey("tag_ref.id"), index=True, nullable=False,
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
    token_address = Column(LargeBinary)
    coins = relationship("Coin")
    market = relationship("Market")


class Quote(Base):
    """Quotes table."""

    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    market_id = Column(Integer, ForeignKey("market.id"), index=True)
    currency = Column(String)
    price = Column(Float, nullable=False)
    vol_24 = Column(Float)
    pct_change_1h = Column(Float)
    pct_change_24h = Column(Float)
    pct_change_7d = Column(Float)
    market_cap = Column(Float)
    fully_diluted_mc = Column(Float)
    last_updated = Column(DateTime, nullable=False)
    market = relationship(
        "Market",
        back_populates="quotes",
    )


def init_db(
    drivername: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
) -> None:
    """
    Initialise the tabales.

    Create the tables in the database according to the datamodel.

    Returns
        NoneType
    """
    # Configure database connection details
    db_config["drivername"] = drivername or db_config.get("drivername")
    db_config["username"] = username or db_config.get("username")
    db_config["password"] = password or db_config.get("password")
    db_config["host"] = host or db_config.get("host")
    db_config["port"] = port or db_config.get("port")
    db_config["database"] = database or db_config.get("database")

    # Build the connection string
    url = URL.create(**db_config)

    # Check whether database exists
    if not database_exists(url):
        click.echo("Creating the database...")
        create_database(url)
        click.echo(f'Database "{url.database}" created.')

    click.echo("Initialising the data model...")

    # Create database engine
    engine = create_engine(url)
    # Initialise tables
    Base.metadata.create_all(engine)

    click.echo("Done.")


def get_data(url: str, /, **kwargs: Any) -> List[Dict[str, Any]]:
    """
    Extract data from URL.

    Parameters
    ----------
        url : str
            URL where to send the request to.

        **kwargs : Any
            Parameters of the `request.get` method.

    Returns
    -------
        List[Dict[str, Any]]
            The data from the API response.

    Raises
    ------
        HTTPError
            * If bad query or problems on server side.

        FileNotFoundError
            * If bad path provided for destination.
    """
    # Send request
    response_raw = requests.get(url, **kwargs)

    # Validate response
    if not response_raw.ok:
        response_raw.raise_for_status()

    content: list = response_raw.json()["data"]
    start = 1
    if kwargs.get("params"):
        start = kwargs["params"].get("start") or start

    while len(content) % 5000 == 0:
        sleep(2)  # Wait for 2 seconds before sending the next request

        # Send requests until data is exhausted
        start += 5000
        if kwargs["params"]:
            kwargs["params"]["start"] = start
        else:
            kwargs["params"] = {"start": start}
        response_raw = requests.get(url, **kwargs)

        # Validate response
        if not response_raw.ok:
            response_raw.raise_for_status()

        new_content = response_raw.json()["data"]
        if new_content:
            content += new_content

    return content


def ingest_data(data: List[dict]) -> None:
    """
    Ingest data into the database.

    Parameters
    ----------
        data : List[dict]
            JSON-like response from the "coinmarketcap" server.

    Returns
    -------
        NoneType
    """
    for entry in data:
        market = Market(
            num_market_pairs=entry["num_market_pairs"],
            date_added=entry["date_added"],
            max_supply=entry["max_supply"],
            circulating_supply=entry["circulating_supply"],
            total_supply=entry["total_supply"],
            cmc_rank=entry["cmc_rank"],
            last_updated=entry["last_updated"],
        )

        if not session.query(Coin).filter(Coin.id == entry["id"]).first():
            coin = Coin(
                id=entry["id"],
                name=entry["name"].lower(),
                symbol=entry["symbol"].lower(),
                slug=entry["slug"].lower(),
            )
            market.coins = coin
            session.add(coin)
        else:
            market.coin_id = entry["id"]

        if entry.get("tags"):
            for tag_data in entry["tags"]:
                tag = Tag()

                tag_reference_query = session.query(TagReference) \
                    .filter(TagReference.name == tag_data.lower()) \
                    .first()
                if not tag_reference_query:
                    tag_reference = TagReference(name=tag_data.lower())
                    tag.tags = tag_reference
                    session.add(tag_reference)
                else:
                    tag.tag_id = tag_reference_query.id

                market.tags.add(tag)
                session.add(tag)

        if entry.get("platform"):
            platform = Platform(
                token_address=entry["platform"]["token_address"].encode(),
            )

            if not session.query(Coin) \
                    .filter(Coin.id == entry["platform"]["id"]).first():
                currency = Coin(
                    id=entry["platform"]["id"],
                    name=entry["platform"]["name"].lower(),
                    symbol=entry["platform"]["symbol"].lower(),
                    slug=entry["platform"]["slug"].lower(),
                )
                platform.coins = currency
                session.add(currency)
            else:
                platform.coin_id = entry["platform"]["id"]

            market.platforms = platform
            session.add(platform)

        if entry.get("quote"):
            for key, value in entry["quote"].items():
                quote = Quote(
                    currency=key,
                    price=value["price"],
                    vol_24=value["volume_24h"],
                    pct_change_1h=value["percent_change_1h"],
                    pct_change_24h=value["percent_change_24h"],
                    pct_change_7d=value["percent_change_7d"],
                    market_cap=value["market_cap"],
                    fully_diluted_mc=value.get("fully_diluted_market_cap"),
                    last_updated=value["last_updated"]
                )
                market.quotes.add(quote)
                session.add(quote)

        session.add(market)
        session.commit()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        format="{asctime} {levelname} {name} % {message}",
        datefmt="%Y-%m-%dT%H:%M:%S",
        style="{",
        level=logging.INFO,
    )

    # Declare constants
    SERVER = "https://web-api.coinmarketcap.com"
    ENDPOINT = "/v1/cryptocurrency/listings/historical"
    URL_CMC = SERVER + ENDPOINT
    CONVERT = "USD,USD,BTC"
    LIMIT = 5000
    # Query date should increment 7 days each new query
    QUERY_DATE = datetime.date(2021, 10, 20)
    # Start should increment 5000 each time there is more than 5k data in the
    # response
    START = 1

    parameters = {
        "convert": CONVERT,
        "date": QUERY_DATE,
        "limit": LIMIT,
        "start": START,
    }
    proxies_list = get_proxies()
    proxies = [
        {"http": f"https://{proxy['IP Address']}:{proxy['Port']}"}
        for proxy in proxies_list
    ] if proxies_list else []
    proxy = proxies[randint(0, len(proxies))] if proxies else {}

    message = {
        "url": URL_CMC,
        "proxy": proxy,
    }

    init_db()

    # Extract data
    try:
        market_data = get_data(URL_CMC, params=parameters, proxies=proxy)
    except requests.models.HTTPError:
        message["status"] = "failure"
        logging.warning(message, exc_info=True)
    else:
        message["status"] = "success"
        logging.info("%s", json.dumps(message, indent=2))

        # Ingest data
        try:
            ingest_data(market_data)
        except Exception:
            err = f"failed data ingestion for {QUERY_DATE}"
            logging.warning(err, exc_info=True)
        else:
            msg = f"ingestion for {QUERY_DATE} is complete"
            logging.info(msg)
