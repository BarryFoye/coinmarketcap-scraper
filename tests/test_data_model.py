"""Test the injection into the data model."""

# Import third-party modules
from data_model.models import Coin, Platform, Quote, Tag

# Import local modules
from . import session

__author__ = "Vitali Lupusor"

data = [
    {
        'id': 1,
        'name': 'Bitcoin',
        'symbol': 'BTC',
        'slug': 'bitcoin',
        'num_market_pairs': None,
        'date_added': '2013-04-28T00:00:00.000Z',
        'tags': [
            'mineable'
        ],
        'max_supply': 21000000,
        'circulating_supply': 11091325,
        'total_supply': 11091325,
        'platform': None,
        'cmc_rank': 1,
        'last_updated': '2013-04-28T23:55:01.000Z',
        'quote': {
            'BTC': {
                'price': 1,
                'volume_24h': 1e-08,
                'percent_change_1h': 0,
                'percent_change_24h': 0,
                'percent_change_7d': 0,
                'market_cap': 11071985.881444559,
                'fully_diluted_market_cap': None,
                'last_updated': '2013-04-29T00:00:01.000Z'
            },
            'USD': {
                'price': 134.210021972656,
                'volume_24h': 0,
                'percent_change_1h': 0.639231,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 1488566971.9558687,
                'last_updated': '2013-04-28T23:55:01.000Z'
            }
        }
    },
    {
        'id': 2,
        'name': 'Litecoin',
        'symbol': 'LTC',
        'slug': 'litecoin',
        'num_market_pairs': None,
        'date_added': '2013-04-28T00:00:00.000Z',
        'tags': [
            'mineable'
        ],
        'max_supply': 84000000,
        'circulating_supply': 17164230,
        'total_supply': 17164230,
        'platform': None,
        'cmc_rank': 2,
        'last_updated': '2013-04-28T23:55:01.000Z',
        'quote': {
            'BTC': {
                'price': 0.03234350781203982,
                'volume_24h': 1e-08,
                'percent_change_1h': 0.799273,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 555151.4070926482,
                'fully_diluted_market_cap': None,
                'last_updated': '2013-04-29T00:00:01.000Z'
            },
            'USD': {
                'price': 4.34840488433838,
                'volume_24h': 0,
                'percent_change_1h': 0.799273,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 74637021.56790735,
                'last_updated': '2013-04-28T23:55:01.000Z'
            }
        }
    },
    {
        'id': 5,
        'name': 'Peercoin',
        'symbol': 'PPC',
        'slug': 'peercoin',
        'num_market_pairs': None,
        'date_added': '2013-04-28T00:00:00.000Z',
        'tags': [
            'mineable'
        ],
        'max_supply': None,
        'circulating_supply': 18757362,
        'total_supply': 18757362,
        'platform': None,
        'cmc_rank': 3,
        'last_updated': '2013-04-28T23:55:03.000Z',
        'quote': {
            'BTC': {
                'price': 0.0028749783046971913,
                'volume_24h': 1e-08,
                'percent_change_1h': -0.934763,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 53927.00880335152,
                'fully_diluted_market_cap': None,
                'last_updated': '2013-04-29T00:00:01.000Z'
            },
            'USD': {
                'price': 0.386524856090546,
                'volume_24h': 0,
                'percent_change_1h': -0.934763,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 7250186.647688276,
                'last_updated': '2013-04-28T23:55:03.000Z'
            }
        }
    },
    {
        'id': 3,
        'name': 'Namecoin',
        'symbol': 'NMC',
        'slug': 'namecoin',
        'num_market_pairs': None,
        'date_added': '2013-04-28T00:00:00.000Z',
        'tags': [
            'mineable'
        ],
        'max_supply': None,
        'circulating_supply': 5415300,
        'total_supply': 5415300,
        'platform': None,
        'cmc_rank': 4,
        'last_updated': '2013-04-28T23:55:02.000Z',
        'quote': {
            'BTC': {
                'price': 0.008235615152382508,
                'volume_24h': 1e-08,
                'percent_change_1h': -0.0505028,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 44598.326734696995,
                'fully_diluted_market_cap': None,
                'last_updated': '2013-04-29T00:00:01.000Z'
            },
            'USD': {
                'price': 1.10723268985748,
                'volume_24h': 0,
                'percent_change_1h': -0.0505028,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 5995997.185385211,
                'last_updated': '2013-04-28T23:55:02.000Z'
            }
        }
    },
    {
        'id': 4,
        'name': 'Terracoin',
        'symbol': 'TRC',
        'slug': 'terracoin',
        'num_market_pairs': None,
        'date_added': '2013-04-28T00:00:00.000Z',
        'tags': [
            'mineable'
        ],
        'max_supply': 42000000,
        'circulating_supply': 2323569.75,
        'total_supply': 2323569.75,
        'platform': None,
        'cmc_rank': 5,
        'last_updated': '2013-04-28T23:55:02.000Z',
        'quote': {
            'BTC': {
                'price': 0.004811595748858439,
                'volume_24h': 1e-08,
                'percent_change_1h': 0.609159,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 11180.078331276067,
                'fully_diluted_market_cap': None,
                'last_updated': '2013-04-29T00:00:01.000Z'
            },
            'USD': {
                'price': 0.646892309188843,
                'volume_24h': 0,
                'percent_change_1h': 0.609159,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 1503099.4011388426,
                'last_updated': '2013-04-28T23:55:02.000Z'
            }
        }
    },
    {
        'id': 7,
        'name': 'Devcoin',
        'symbol': 'DVC',
        'slug': 'devcoin',
        'num_market_pairs': None,
        'date_added': '2013-04-28T00:00:00.000Z',
        'tags': [
            'mineable'
        ],
        'max_supply': None,
        'circulating_supply': 4366620160,
        'total_supply': 4366620160,
        'platform': None,
        'cmc_rank': 6,
        'last_updated': '2013-04-28T23:55:14.000Z',
        'quote': {
            'BTC': {
                'price': 2.4257628562665444e-06,
                'volume_24h': 1e-08,
                'percent_change_1h': 0.461694,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 10592.384991552675,
                'fully_diluted_market_cap': None,
                'last_updated': '2013-04-29T00:00:01.000Z'
            },
            'USD': {
                'price': 0.000326130335452035,
                'volume_24h': 0,
                'percent_change_1h': 0.461694,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 1424087.2975724188,
                'last_updated': '2013-04-28T23:55:14.000Z'
            }
        }
    },
    {
        'id': 6,
        'name': 'Novacoin',
        'symbol': 'NVC',
        'slug': 'novacoin',
        'num_market_pairs': None,
        'date_added': '2013-04-28T00:00:00.000Z',
        'tags': ['mineable'],
        'max_supply': None,
        'circulating_supply': 273705.9375,
        'total_supply': 273705.9375,
        'platform': None,
        'cmc_rank': 7,
        'last_updated': '2013-04-28T23:55:03.000Z',
        'quote': {
            'BTC': {
                'price': 0.03158483190407031,
                'volume_24h': 1e-08,
                'percent_change_1h': 2.13819,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 8644.956027083475,
                'fully_diluted_market_cap': None,
                'last_updated': '2013-04-29T00:00:01.000Z'
            },
            'USD': {
                'price': 4.24640512466431,
                'volume_24h': 0,
                'percent_change_1h': 2.13819,
                'percent_change_24h': None,
                'percent_change_7d': None,
                'market_cap': 1162266.2956510494,
                'last_updated': '2013-04-28T23:55:03.000Z'
            }
        }
    },
    {
        "id": 825,
        "name": "Tether",
        "symbol": "USDT",
        "slug": "tether",
        "num_market_pairs": 18771,
        "date_added": "2015-02-25T00:00:00.000Z",
        "tags": [
            "payments",
            "stablecoin",
            "stablecoin-asset-backed",
            "binance-smart-chain",
            "avalanche-ecosystem",
            "solana-ecosystem"
        ],
        "max_supply": None,
        "circulating_supply": 69043109914.2716,
        "total_supply": 71382497034.74619,
        "platform": {
            "id": 1027,
            "name": "Ethereum",
            "symbol": "ETH",
            "slug": "ethereum",
            "token_address": "0xdac17f958d2ee523a2206206994597c13d831ec7"
        },
        "cmc_rank": 5,
        "last_updated": "2021-10-20T23:00:00.000Z",
        "quote": {
            "BTC": {
                "price": 1.5152255792190473e-05,
                "volume_24h": 1063568.7000611362,
                "percent_change_1h": 0.016157808294,
                "percent_change_24h": -0.017622106384,
                "percent_change_7d": -0.015634486349,
                "market_cap": 1046158.8621093656,
                "fully_diluted_market_cap": None,
                "last_updated": "2021-10-20T23:59:02.000Z"
            },
            "USD": {
                "price": 0.999940347223595,
                "volume_24h": 70187915899.85,
                "percent_change_1h": 0.016157808294,
                "percent_change_24h": -0.017622106384,
                "percent_change_7d": -0.015634486349,
                "market_cap": 69038991301.0736,
                "last_updated": "2021-10-20T23:00:00.000Z"
            }
        }
    }

]

for entry in data:
    coin = Coin(
        id=entry["id"],
        name=entry["name"],
        symbol=entry["symbol"],
        slug=entry["slug"],
        num_market_pairs=entry["num_market_pairs"],
        date_added=entry["date_added"],
        max_supply=entry["max_supply"],
        circulating_supply=entry["circulating_supply"],
        total_supply=entry["total_supply"],
        cmc_rank=entry["cmc_rank"],
        last_updated=entry["last_updated"],
    )

    if entry.get("tags"):
        for tag_data in entry["tags"]:
            tag = Tag(tag=tag_data)
            coin.tags.add(tag)
            session.add(tag)

    if entry.get("platform"):
        platform = Platform(
            id=entry["platform"]["id"],
            name=entry["platform"]["name"],
            symbol=entry["platform"]["symbol"],
            slug=entry["platform"]["slug"],
            token_address=entry["platform"]["token_address"],
        )
        coin.platforms.add(platform)
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
            coin.quotes.add(quote)
            session.add(quote)

    session.add(coin)
    session.commit()
