"""TODO: Add description."""

# Import standard modules
import datetime as dt
import json
import logging
from random import randint

# Import third-party modules
import click
import requests

# Import local modules
from . import get_data, ingest_data
from .helpers import get_proxies


@click.group()
def cli():
    """Command line interface for `cmc_scraper` module."""
    ...


@cli.command()
def populate_history() -> None:
    """Populate the database with data starting from 2013-04-28."""
    # Declare constants
    server = "https://web-api.coinmarketcap.com"
    endpoint = "/v1/cryptocurrency/listings/historical"
    url_coinmarketcap = server + endpoint
    convert = "USD,USD,BTC"
    limit = 5000
    # Query date should increment 7 days each new query
    query_date = dt.date(2013, 4, 28)
    # Start should increment 5000 each time there is more than 5k data in the
    # response
    start = 1

    # Acquire a list of proxy servers
    proxies_list = get_proxies()
    proxies = [
        {"http": f"https://{proxy['IP Address']}:{proxy['Port']}"}
        for proxy in proxies_list
    ] if proxies_list else []
    proxy = proxies[randint(0, len(proxies))] if proxies else {}

    # Configure request parameters
    parameters = {
        "convert": convert,
        "date": query_date,
        "limit": limit,
        "start": start,
    }

    # Configure default logging message
    message = {
        "url": url_coinmarketcap,
        "parameters": parameters,
        "proxy": proxy,
    }

    while query_date < dt.datetime.today():
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
            logging.info("%s", json.dumps(message, indent=2))

            # Ingest data
            try:
                ingest_data(currency_data)
            except Exception:
                err = f"failed data ingestion for {query_date}"
                logging.warning(err, exc_info=True)
            else:
                msg = f"ingestion for {query_date} is complete."
                logging.info(msg)

        query_date += dt.timedelta(7)


@cli.command()
def populate_latest() -> None:
    """Populate the database with the latest data."""
    ...


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        format="{asctime} {levelname} {name} % {message}",
        datefmt="%Y-%m-%dT%H:%M:%S",
        style="{",
        level=logging.INFO,
    )

    # Execute command
    cli()
