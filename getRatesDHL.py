import os
import requests
import base64
from getRatesShippo import *
import json
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DHL_KEY")
api_secret = os.getenv("DHL_SECRET")

credentials = f"{api_key}:{api_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# real URL ==> url = "https://express.api.dhl.com/mydhlapi/rates"
url = "https://express.api.dhl.com/mydhlapi/test/rates"

def get_rates_from_dhl():
    params = {
        "accountNumber": "423261594",
        "originCountryCode": "CZ",
        "originCityName": "Prague",
        "originPostalCode": "14800",
        "destinationCountryCode": "US",
        "destinationCityName": "New York",
        "destinationPostalCode": "10001",
        "weight": 10.5,
        "length": 25,
        "width": 35,
        "height": 15,
        "plannedShippingDate": "2026-06-20",
        "unitOfMeasurement": "metric",
        "isCustomsDeclarable": "false",
        "nextBusinessDay": "false"
    }

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(url, headers=headers, params=params)

    console = Console()
    data = response.json()

    table = Table(title="DHL Rates", header_style="bold magenta")
    table.add_column("Service")
    table.add_column("Delivery Days", justify="center")
    table.add_column("Price",         justify="right", style="bold green")

    for product in data.get("products", []):
        price    = product.get("totalPrice", [{}])[0]
        delivery = product.get("deliveryCapabilities", {})

        table.add_row(
           f"DHL EXPRESS {product.get("productName", "")}",
            str(delivery.get("totalTransitDays", "")),
            f"{price.get('price', '')} {price.get('priceCurrency', '')}"
        )

    console.print(table)

    # print(json.dumps(data, indent=2))


if __name__ == "__main__":
    get_rates_from_dhl()
    # get_rates_from_shippo()