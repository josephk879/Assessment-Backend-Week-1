"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime, date

from flask import Flask, Response, request, jsonify

from date_functions import (convert_to_datetime, get_day_of_week_on,
                            get_days_between, get_current_age)

app_history = []

app = Flask(__name__)


def add_to_history(current_request):
    """Adds a route to the app history."""
    app_history.append({
        "method": current_request.method,
        "at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "route": current_request.endpoint
    })


def clear_history():
    """Clears the app history."""
    app_history.clear()


@app.get("/")
def index():
    """Returns an API welcome message."""
    return jsonify({"message": "Welcome to the Days API."})


@app.post("/between")
def days_between() -> dict:
    """Returns the number of days between two dates."""
    days_data = request.json
    if len(days_data) < 2:
        return {"error": "Missing required data."}, 400

    if "first" not in days_data and "last" not in days_data:
        return {"error": "Missing required data."}, 400

    for data in days_data.values():
        if not isinstance(data, str):
            return {"error": "Missing required data."}, 400

    try:
        first_date = convert_to_datetime(days_data["first"])

    except ValueError:
        return {
            "error": "Unable to convert value to datetime."
        }, 400

    try:
        last_date = convert_to_datetime(days_data["last"])

    except ValueError:
        return {
            "error": "Unable to convert value to datetime."
        }, 400

    add_to_history(request)

    return jsonify({"days": get_days_between(first_date, last_date)})


@app.post("/weekday")
def day_of_the_week():
    """Returns the day of the week a specific day is."""
    date = request.json
    if len(date) == 0:
        return {"error": "Missing required data."}, 400
    if "date" not in date:
        return {"error": "Missing required data."}, 400

    try:
        date = convert_to_datetime(date["date"])
    except ValueError:
        return {
            "error": "Unable to convert value to datetime."
        }

    add_to_history(request)
    return jsonify({"weekday", get_day_of_week_on(date)})


@app.route("/history", methods=["GET", "DELETE"])
def previous_requests():
    """Returns details on the last `number` of requests to the API
    or
    deletes details of all previous requests to the API."""
    if request.method == "DELETE":
        app_history.clear()
        return {"status": "History cleared"}, 200

    elif request.method == "GET":
        number = request.args.get("number", 5)

        if not isinstance(number, int):
            return {
                "error": "Number must be an integer between 1 and 20."}, 400

        if number < 1 or number > 20:
            return {
                "error": "Number must be an integer between 1 and 20."}, 400

        add_to_history(request)

        recent_requests = app_history[-number:]
        return recent_requests[::-1], 200


[{"method": "POST", "at": "12/02/2023 18:39", "route": "weekday"},
    {"method": "POST", "at": "12/02/2023 18:36", "route": "weekday"}]


@app.get("/current_age")
def current_age():
    """Returns a current age in years based on a given birthdate."""
    birthdate = request.json
    if not isinstance(birthdate, date):
        return {
            "error": "Value for date parameter is invalid."
        }


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
