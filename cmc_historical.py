# First we need to generate the date in the YYYY-MM-DD format
# It should start at 2013-04-28 and run to current day

import datetime as dt
import requests
import json

CONVERT = "USD,USD,BTC"
LIMIT = 5000

# Query date should increment 7 days each new query
query_date = dt.date(2013, 4, 28)
# Start should increment 5000 each time there is more than 5k data in the response
start = 1

query = (f"https://web-api.coinmarketcap.com/v1/cryptocurrency/listings/historical?"
         f"convert={CONVERT}&date={query_date}&limit={LIMIT}&start={start}")

try:
    def get_data(query=None):
        response_raw = requests.get(query)
        objects = response_raw.json()["data"]
        with open("data.json", "w") as json_file:
            json.dump(objects, json_file, indent=4)
except Exception:
    print("We have a problem")

# Entrypoint
if __name__ == '__main__':
    get_data(query)
