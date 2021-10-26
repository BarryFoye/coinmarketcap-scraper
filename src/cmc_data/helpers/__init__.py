"""Collection of helper functions."""

# Import standard modules
from typing import List, Optional

# Import third-party modules
import requests
from bs4 import BeautifulSoup


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
