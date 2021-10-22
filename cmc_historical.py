"""
First we need to generate the date in the YYYY-MM-DD format.

It should start at 2013-04-28 and run to current day.

TODO:
    1. Write a function that will ingest the retrieved data into a database
    1. Write a function that would retrieve all data from 2013-04-28 onwards
    1. Write a function that will only trieve the last 7 days of data
"""

# Import standard modules
import datetime as dt
import json
import logging
from random import randint
from time import sleep
from typing import Any, Dict, List, Optional

# Import third-party modules
import requests
from bs4 import BeautifulSoup


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


def get_proxy() -> Optional[List[dict]]:
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
    URL = SERVER + ENDPOINT
    CONVERT = "USD,USD,BTC"
    LIMIT = 5000
    # Query date should increment 7 days each new query
    QUERY_DATE = dt.date(2013, 4, 28)
    # Start should increment 5000 each time there is more than 5k data in the
    # response
    START = 1

    parameters = {
        "convert": CONVERT,
        "date": QUERY_DATE,
        "limit": LIMIT,
        "start": START,
    }
    proxies_list = get_proxy()
    proxies = [
        {"http": f"https://{proxy['IP Address']}:{proxy['Port']}"}
        for proxy in proxies_list
    ] if proxies_list else []
    proxy = proxies[randint(0, len(proxies))] if proxies else {}

    message = {
        "url": URL,
        "proxy": proxy,
    }

    try:
        data = get_data(URL, params=parameters, proxies=proxy)
    except requests.models.HTTPError:
        message["status"] = "failure"
        logging.warning(message, exc_info=True)
    else:
        message["status"] = "success"
        logging.info("%s", json.dumps(message, indent=2))
        print(data)  # TODO: Replace this with data the ingestion function
