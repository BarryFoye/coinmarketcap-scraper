"""
Coinmarketcap scraper.

Scrape data from https://coinmarketcap.com and populate the database.
"""

# Import standard modules
import logging
from time import sleep
from typing import Any, Dict, List

# Import third-party modules
import requests

# Import local modules
from data_model import session
from data_model.models import Coin, Market, Platform, Quote, Tag, TagReference


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

        except Exception:
            logging.warning(
                "entry failed validation: %s", entry, exc_info=True,
            )
        else:
            session.add(market)
            session.commit()
