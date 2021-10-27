"""Collection of helper functions."""

# Import standard modules
import datetime
from typing import List, Optional, Union

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


def validate_date_input(
    date: Union[str, datetime.date, datetime.datetime]
) -> datetime.date:
    """
    Validate date inputs.

    IMPORTANT!
    The input date value must be between 2013-04-28 and current date.

    Parameters
    ----------
        date : str, datetime.date, datetime.datetime
            If `date` is of type `<class str>`, then it should conform to one
            of the following date formats:
                * %Y-%m-%d (i.e. 2000-01-01)
                * %Y/%m/%d (i.e. 2000/01/01)
                * %d-%m-%Y (i.e. 01-01-2000)
                * %d/%m/%Y (i.e. 01/01/2000)

    Returns
    -------
        datetime.date
            If validation is successful.

    Raises
    ------
        TypeError
            * If `date` parameter not of type `str` or `datetime.datetime`.

        ValueError
            * If `date` is prior to 2013-04-28.
    """
    _date = None
    if isinstance(date, str):
        valid_date_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
        for index, date_format in enumerate(valid_date_formats):
            try:
                _date = datetime.datetime.strptime(date, date_format).date()
            except ValueError as err:
                if index == len(valid_date_formats) - 1:
                    message = (
                        f'incorrect date format of `date` parameter "{date}". '
                        "Expected one of the following formats: "
                        f"{valid_date_formats}"
                    )
                    raise ValueError(message) from err
            else:
                break
    elif isinstance(date, datetime.date):
        _date = date
    elif isinstance(date, datetime.datetime):
        _date = date.date()
    else:
        raise TypeError((
            f"incorrect type of `date` parameter: {type(date)}. Expected "
            "one of the following: [<class str>, <class datetime.datetime>]"
        ))

    if not datetime.datetime(2013, 4, 28) < _date < datetime.datetime.today():
        raise ValueError((
            "`date` parameter should be greater than 2013-04-28 and less than "
            "date at runtime"
        ))

    return _date
