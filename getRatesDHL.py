import os
import requests
import base64
from dotenv import load_dotenv
from userInputDataClass import ShippingRequest

load_dotenv()

api_key = os.getenv("DHL_KEY")
api_secret = os.getenv("DHL_SECRET")

credentials = f"{api_key}:{api_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

# test URL ==> url = "https://express.api.dhl.com/mydhlapi/test/rates"
url = "https://express.api.dhl.com/mydhlapi/rates"

def get_rates_from_dhl(dto: ShippingRequest):
    params = {
        "accountNumber": dto.dhl_account_number,
        "originCountryCode": dto.both_from_country_code,
        "originCityName": dto.both_from_city,
        "originPostalCode": dto.both_from_zip,
        "destinationCountryCode": dto.country_to,
        "destinationCityName": dto.city_to,
        "destinationPostalCode": dto.postal_code_to,
        "weight": dto.weight,
        "length": dto.length,
        "width": dto.width,
        "height": dto.height,
        "plannedShippingDate": dto.dhl_planned_shipping_date,
        "unitOfMeasurement": dto.dhl_unit_of_measurement,
        "isCustomsDeclarable": dto.dhl_is_customs_declarable,
        "nextBusinessDay": dto.dhl_is_next_business_day,

    }

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(url, headers=headers, params=params, timeout=15)
    response.raise_for_status()
    ## I capture the API response and deserialize it
    api_response_data = response.json()
    ## I return it
    return api_response_data

if __name__ == "__main__":
    get_rates_from_dhl()
