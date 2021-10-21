"""
First we need to generate the date in the YYYY-MM-DD format.

It should start at 2013-04-28 and run to current day.
"""

# Import standard modules
import datetime as dt
import json
import logging
import sys
from os import path
from typing import Any, Optional

# Import third-party modules
import requests


def get_data(
    url: str, destination: Optional[str] = None, /, **kwargs: Any
) -> None:
    """
    Extract data from URL.

    Parameters
    ----------
        url : str
            URL where to send the request to.

        destination : str, None
            Path where to write the file to.
            If destination not provided, writes to current working directory.

        **kwargs : Any
            Parameters of the `request.get` method.

    Returns
    -------
        NoneType

    Raises
    ------
        HTTPError
            * If bad query or problems on server side.

        FileNotFoundError
            * If bad path provided for destination.
    """
    # Validate destination
    basename = f"data_{dt.datetime.now():%Y%m%dT%H%M%S}.json"
    if destination:
        dirname = path.dirname(destination)
        # If provided destination path is a directory, use default basename
        if path.isdir(destination):
            destination = path.join(destination, basename)
        # Else, if the path is supposed to include basename, check the validity
        # of the dirname
        elif (not path.isdir(dirname)) and dirname:
            logging.critical('"%s" does not exist', dirname)
            sys.exit(1)
    else:
        # If no destination path provided, write to current working directory
        # with default basename value
        destination = basename

    # Send request
    response_raw = requests.get(url, **kwargs)

    # Validate response
    if response_raw.status_code != 200:
        response_raw.raise_for_status()

    # Write data to disk
    with open(destination, "w") as json_file:
        json.dump(response_raw.json()["data"], json_file, indent=4)


if __name__ == '__main__':
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
    DESTINATION = (
        f"coinmarketcap_{dt.datetime.now():%Y%m%dT%H%M%S}_"
        f"{CONVERT.replace(',', '_')}_{QUERY_DATE}.json"
    )

    parameters = {
        "convert": CONVERT,
        "date": QUERY_DATE,
        "limit": LIMIT,
        "start": START,
    }

    message = {
        "url": URL,
        "destination": DESTINATION,
    }

    try:
        get_data(
            URL,
            DESTINATION,
            params=parameters,
        )
    except requests.models.HTTPError:
        message["status"] = "failure"
        logging.warning(message, exc_info=True)
    else:
        message["status"] = "success"
        logging.info("%s", json.dumps(message, indent=2))
