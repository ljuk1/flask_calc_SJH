import os
import requests
from pprint import pprint
from dotenv import load_dotenv

from rich import print_json, pretty
from rich.console import Console
from rich.table import Table
from userInputDataClass import *

load_dotenv()
pretty.install()

## LOAD UP API KEYS + URL ENDPOINT

SHIPPO_API_KEY = os.getenv("SHIPPO_API_KEY")
if not SHIPPO_API_KEY:
    raise SystemExit("The key is broken!")

SHIPPO_URL = "https://api.goshippo.com/shipments/"



## CREATE AN ORDER

def get_rates_from_shippo(dto:ShippingRequest):
    headers = {
        "Authorization": f"ShippoToken {SHIPPO_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "address_to":{
            "country": dto.country_to,
            "name": dto.name_to,
            "street1": dto.street_to,
            "city": dto.city_to,
            "zip": dto.postal_code_to,
        },
        "address_from": {
            "country": dto.both_from_country_code,
            "name": dto.shippo_name_from,
            "street1": dto.shippo_street_from,
            "city": dto.both_from_city,
            "zip": dto.both_from_zip,
        },
        "parcels": [{

            "mass_unit": dto.shippo_mass_unit,
            "distance_unit": dto.shippo_distance_unit,
            "length": dto.length,
            "width": dto.width,
            "height": dto.height,
            "weight": dto.weight,

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