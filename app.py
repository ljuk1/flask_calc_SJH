import os
from pprint import pprint
from flask import Flask, render_template, request, url_for, redirect, flash
# CUSTOM DTO IMPORT
from userInputDataClass import ShippingRequest
# CUSTOM METHOD IMPORTS
from getRatesShippo import get_rates_from_shippo
from getRatesDHL import get_rates_from_dhl
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user import User

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


## LOG IN/OUT ROUTE
app = Flask(__name__)
# session cookie key
app.secret_key = os.getenv("FLASK_SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY not set")
#

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
limiter = Limiter(get_remote_address, app=app, default_limits=["500 per day"])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(username):
    return User(username)

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("300 per day")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("calculator"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if User.validate(username, password):
            login_user(User(username))
            return redirect(url_for("calculator"))
        flash("Wrong username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


## CALCULATOR PAGE ROUTE
@app.route("/", methods=["GET", "POST"])
@login_required
def calculator():
    shippo_rates = None
    dhl_rates = None

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
        shippo_rates = get_rates_from_shippo(user_input_dto).get("rates", [])
        # pprint(shippo_rates.get("rates", []))
        dhl_rates = get_rates_from_dhl(user_input_dto).get("products", [])
        # pprint(dhl_rates.get("products", []))


    return render_template("calculator.html", shippo_rates = shippo_rates, dhl_rates = dhl_rates)



if __name__ == '__main__':
    app.run(debug=False, port=5001)
