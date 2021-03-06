"""
Coinmarketcap scraper.

Scrape data from https://coinmarketcap.com and populate the database.
"""

# Import standard modules
import json
import logging
import datetime
from time import sleep
from typing import Any, Dict, List, Optional, Union

# Import third-party modules
import requests

# Import local modules
from cmc_data.data_model import session
from cmc_data.data_model.models import (
    Coin, Market, Platform, Quote, Tag, TagReference,
)
from cmc_data.helpers import validate_date_input


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
        try:
            market = Market(
                num_market_pairs=entry["num_market_pairs"],
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
                    date_added=entry["date_added"],
                    max_supply=entry["max_supply"],
                )
                market.coins = coin
                session.add(coin)
            else:
                market.coin_id = entry["id"]

            if entry.get("platform"):
                if not session.query(Coin) \
                        .filter(Coin.id == entry["platform"]["id"]).first():
                    currency = Coin(
                        id=entry["platform"]["id"],
                        name=entry["platform"]["name"].lower(),
                        symbol=entry["platform"]["symbol"].lower(),
                        slug=entry["platform"]["slug"].lower(),
                    )
                    session.add(currency)

                if not session.query(Platform) \
                        .filter(Platform.id == entry["id"]).first():
                    platform = Platform(
                        id=entry["id"],
                        platform_id=entry["platform"]["id"],
                        token_address=entry["platform"]["token_address"]
                        .encode(),
                    )
                    session.add(platform)

            if entry.get("tags"):
                for tag_data in entry["tags"]:
                    tag = Tag(coin_id=entry["id"])

                    tag_reference_query = session.query(TagReference) \
                        .filter(TagReference.name == tag_data.lower()) \
                        .first()
                    if not tag_reference_query:
                        tag_reference = TagReference(name=tag_data.lower())
                        tag.tags = tag_reference
                        session.add(tag_reference)
                    else:
                        tag.tag_id = tag_reference_query.id

                    session.add(tag)

            if entry.get("quote"):
                for key, value in entry["quote"].items():
                    quote = Quote(
                        coin_id=entry["id"],
                        currency=key,
                        price=value.get("price"),
                        vol_24=value.get("volume_24h"),
                        pct_change_1h=value.get("percent_change_1h"),
                        pct_change_24h=value.get("percent_change_24h"),
                        pct_change_7d=value.get("percent_change_7d"),
                        market_cap=value.get("market_cap"),
                        fully_diluted_mc=value.get("fully_diluted_market_cap"),
                        last_updated=value.get("last_updated")
                    )
                    session.add(quote)

        except Exception:
            session.rollback()
            logging.warning(
                "entry failed validation: %s", entry, exc_info=True,
            )
        else:
            session.add(market)
            session.commit()


def populate(
    date: Union[str, datetime.date, datetime.datetime],
    proxy: Optional[dict] = None
) -> None:
    """
    Extract data from source and ingest into the data model.

    Parameters
    ----------
        date : str, datetime.date, datetime.datetime
            The date for which to retrieve the data.

        proxy : dict, NoneType
            Proxy server. Default `None`.

    Returns
    -------
        NoneType

    Raises
    ------
        TypeError
            * If input parameters of incorrect type.

        ValueError
            * If `date` is prior to 2013-04-28.
    """
    # Validate parameters
    _date = validate_date_input(date)

    # Declare variables
    server = "https://web-api.coinmarketcap.com"
    endpoint = "/v1/cryptocurrency/listings/historical"
    url_coinmarketcap = server + endpoint
    convert = "USD,USD,BTC"
    limit = 5000
    start = 1

    # Configure request parameters
    parameters = {
        "convert": convert,
        "date": _date,
        "limit": limit,
        "start": start,
    }

    # Configure default logging message
    message: dict = {
        "url": url_coinmarketcap,
        "parameters": parameters,
        "proxy": proxy,
    }

    # Extract data
    try:
        currency_data = get_data(
            url_coinmarketcap, params=parameters, proxies=proxy,
        )
    except requests.models.HTTPError:
        message["status"] = "failure"
        logging.warning(message, exc_info=True)
    else:
        message["status"] = "success"
        message["parameters"]["date"] = str(message["parameters"]["date"])
        logging.info("%s", json.dumps(message, indent=2))

        # Ingest data
        try:
            ingest_data(currency_data)
        except Exception:
            err = f"failed data ingestion for {_date:%Y-%m-%d}"
            logging.warning(err, exc_info=True)
        else:
            msg = f"ingestion for {_date:%Y-%m-%d} is complete."
            logging.info(msg)


del Any, Dict, List, datetime  # Clean up
