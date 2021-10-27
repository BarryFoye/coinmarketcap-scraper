"""TODO: Add description."""

# Import standard modules
import datetime as dt
import logging
from random import randint

# Import third-party modules
import click

# Import local modules
from . import populate
from .helpers import get_proxies


@click.group()
def cli():
    """Command line interface for `cmc_data` module."""
    ...


@cli.command()
def populate_historical() -> None:
    """Populate the database with data starting from 2013-04-28."""
    # Declare variables
    query_date = dt.date(2013, 4, 28)

    # Acquire a list of proxy servers
    proxies_list = get_proxies()
    proxies = [
        {"http": f"https://{proxy['IP Address']}:{proxy['Port']}"}
        for proxy in proxies_list
    ] if proxies_list else []

    # Extract historical data and populate talbes
    while query_date < dt.datetime.today():
        proxy = proxies[randint(0, len(proxies))] if proxies else {}
        populate(query_date, proxy)
        query_date += dt.timedelta(7)


@cli.command()
def populate_latest() -> None:
    """Populate the database with the latest data."""
    # Declare variables
    query_date = dt.datetime.today().date() - dt.timedelta(1)

    # Acquire a list of proxy servers
    proxies_list = get_proxies()
    proxies = [
        {"http": f"https://{proxy['IP Address']}:{proxy['Port']}"}
        for proxy in proxies_list
    ] if proxies_list else []
    proxy = proxies[randint(0, len(proxies))] if proxies else {}

    # Extract latest data and populate talbes
    populate(query_date, proxy)


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
