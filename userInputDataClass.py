
from dataclasses import dataclass, field
from datetime import date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ShippingRequest:

## == MANUAL USER INPUT ==
    # SHIPPING TO
    country_to: str
    city_to: str
    street_to: str
    postal_code_to: str
    name_to: str

    # PACKAGE
    weight: float
    length: int
    width: int
    height: int
## END == MANUAL USER INPUT ==



    #### computed each time at instantiation
    ### could use timedelta(days=x) to move the planned shipping project_data into future if that follows the business logic closer
    dhl_planned_shipping_date: str = field(default_factory=lambda: (date.today().isoformat()))


    # .env hard-coded options
    dhl_account_number: str = os.getenv("DHL_ACCOUNT_NUMBER")
    shippo_mass_unit: str = os.getenv("SHIPPO_MASS_UNIT")
    shippo_distance_unit: str = os.getenv("SHIPPO_DISTANCE_UNIT")
    both_from_country_code: str = os.getenv("BOTH_FROM_COUNTRY_CODE")
    both_from_city: str = os.getenv("BOTH_FROM_CITY")
    both_from_zip: str = os.getenv("BOTH_FROM_ZIP")
    shippo_name_from: str = os.getenv("SHIPPO_NAME_FROM")
    shippo_street_from: str = os.getenv("SHIPPO_STREET_FROM")
    dhl_unit_of_measurement: str = os.getenv("DHL_UNIT_OF_MEASURMENT")
     # END === .env hard-coded options === END


# DHL TOGGLE OPTIONS
    dhl_is_customs_declarable: str = "false"
    dhl_is_next_business_day: str = "false"


#PAYLOADS BEING MODELLED
# WHERE payload=shippo

# payload = {
#    "address_to":{
#        "country": "GB",
#        "name": "Lukasz",
#        "street1": "Lytton Avenue 80",
#        "city": "London",
#        "zip": "EN36EN",
#    },
#    "address_from": {
#        "country": "GB",
#        "name": "lukasz",
#        "street1": "Donard Crescent 6",
#        "city": "Annalong",
#        "zip": "BT344RS",
#    },
#    "parcels": [{
#
#
#        "mass_unit": "kg",
#        "distance_unit": "cm",
#        "length": 10,
#        "width": 10,
#        "height": 10,
#        "weight": 1,
#
#
#    }]
# }
# def get_rates_from_dhl():
#    params = {
#        "accountNumber": "423261594",
#        "originCountryCode": "CZ",
#        "originCityName": "Prague",
#        "originPostalCode": "14800",
#        "destinationCountryCode": "US",
#        "destinationCityName": "New York",
#        "destinationPostalCode": "10001",
#        "weight": 10.5,
#        "length": 25,
#        "width": 35,
#        "height": 15,
#        "plannedShippingDate": "2026-06-20",
#        "unitOfMeasurement": "metric",
#        "isCustomsDeclarable": "false",
#        "nextBusinessDay": "false"




