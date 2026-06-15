import os
import requests
from pprint import pprint
from dotenv import load_dotenv

from rich import print_json, pretty
from rich.console import Console
from rich.table import Table

load_dotenv()
pretty.install()

## LOAD UP API KEYS + URL ENDPOINT

SHIPPO_API_KEY = os.getenv("SHIPPO_API_KEY")
if not SHIPPO_API_KEY:
    raise SystemExit("The key is broken!")

SHIPPO_URL = "https://api.goshippo.com/shipments/"



## CREATE AN ORDER

def get_rates_from_shippo():
    headers = {
        "Authorization": f"ShippoToken {SHIPPO_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "address_to":{
            "country": "GB",
            "name": "lukasz",
            "street1": "Lytton Avenue 80",
            "city": "London",
            "zip": "EN36EN",
        },
        "address_from": {
            "country": "GB",
            "name": "lukasz",
            "street1": "Donard Crescent 6",
            "city": "Annalong",
            "zip": "BT344RS",
        },
        "parcels": [{

            "mass_unit": "kg",
            "distance_unit": "cm",
            "length": 10,
            "width": 10,
            "height": 10,
            "weight": 1,

        }]
    }

    ##
    response_to_get_rates = requests.post(SHIPPO_URL, json=payload, headers=headers)
    response_to_get_rates_deserialised = response_to_get_rates.json()

    console = Console()
    table = Table(title="Shippo Rates", header_style="bold magenta")

    table.add_column("Provider")
    table.add_column("Service")
    table.add_column("Amount", justify="right")
    table.add_column("Days", justify="right")

    for rate in response_to_get_rates_deserialised.get("rates", []):
        table.add_row(
            rate["provider"],
            rate["servicelevel"]["name"],
            rate["amount"],
            str(rate["estimated_days"]),
        )

    console.print(table)
    ## this is actually where the response from shippo goes json --> python
    return response_to_get_rates_deserialised


if __name__ == "__main__":
    get_rates_from_shippo()