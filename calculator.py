import os
import requests
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()


## LOAD UP API KEYS + URL ENDPOINT

SHIPPO_API_KEY = os.getenv("SHIPPO_API_KEY")
if not SHIPPO_API_KEY:
    raise SystemExit("The key is broken!")

SHIPPO_URL = "https://api.goshippo.com/orders/"



## CREATE AN ORDER

def create_order_for_shippo():
    headers = {
        "Authorization": f"ShippoToken {SHIPPO_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "to_address":{
            "country": "PL"
        },

        "line_items":[
            {
            "quantity": 1,
            "title": "Order to call the compare rates end-point",
            "weight": 1,
            "weight_unit": "kg",

            }
        ],
        "placed_at": "2016-09-23T01:28:12Z",
        "weight": 1,
        "weight_unit": "kg",
}

    ##
    response_to_create_order = requests.post(SHIPPO_URL, json=payload, headers=headers)

    pprint(response_to_create_order.json())
    ## this is actually where the response from shippo goes json --> python
    return response_to_create_order.json()


if __name__ == "__main__":
    create_order_for_shippo()