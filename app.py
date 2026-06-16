from pprint import pprint
from flask import Flask, render_template, request
from userInputDataClass import ShippingRequest
from getRatesShippo import get_rates_from_shippo

app = Flask(__name__)

## CALCULATOR PAGE ROUTE
@app.route("/", methods=["GET", "POST"])
def calculator():
    if request.method == "POST":
        user_input_dto = ShippingRequest(
        country_to=request.form["country_to"],
        city_to=request.form["city_to"],
        street_to=request.form["street_to"],
        postal_code_to=request.form["postal_code_to"],
        name_to=request.form["name_to"],
        weight=float(request.form["weight"]),
        length=int(request.form["length"]),
        width=int(request.form["width"]),
        height=int(request.form["height"]),
        dhl_is_customs_declarable=request.form["dhl_is_customs_declarable"],
        dhl_is_next_business_day=request.form["dhl_is_next_business_day"],

        ### the rest of fields are from .env, instantiated to default automatically
        )
        pprint(user_input_dto.__dict__)
        shippo_rates = get_rates_from_shippo(user_input_dto)
        pprint(shippo_rates.get("rates", []))

    return render_template("calculator.html")



if __name__ == '__main__':
    app.run(debug=True, port=5001)
