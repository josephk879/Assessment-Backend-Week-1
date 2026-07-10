"""This file defines the API routes."""

# pylint: disable = no-name-in-module

from datetime import datetime

from flask import Flask, request, jsonify

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
def between() -> dict:
    """Returns the number of days between two dates."""
    days_data = request.json
    if len(days_data) < 2:
        return {"error": "Missing required data."}, 400

    if "first" not in days_data and "last" not in days_data:
        return {"error": "Missing required data."}, 400

    for data in days_data.values():
        if not isinstance(data, str):
            return {
                "error": "Unable to convert value to datetime."
            }, 400

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
def weekday():
    """Returns the day of the week a specific day is."""
    specific_date = request.json
    if len(specific_date) == 0:
        return {"error": "Missing required data."}, 400
    if "date" not in specific_date:
        return {"error": "Missing required data."}, 400

    if not isinstance(specific_date["date"], str):
        return {
            "error": "Unable to convert value to datetime."
        }, 400

    try:
        specific_date = convert_to_datetime(specific_date["date"])
    except ValueError:
        return {
            "error": "Unable to convert value to datetime."
        }, 400

    add_to_history(request)
    return {"weekday": get_day_of_week_on(specific_date)}


@app.route("/history", methods=["GET", "DELETE"])
def previous_requests():
    """Returns details on the last `number` of requests to the API
    or
    deletes details of all previous requests to the API."""
    if request.method == "DELETE":
        app_history.clear()
        return {"status": "History cleared"}, 200

    elif request.method == "GET":
        try:
            number = int(request.args.get("number", 5))

        except ValueError:
            return {
                "error": "Number must be an integer between 1 and 20."}, 400

        if number < 1 or number > 20:
            return {
                "error": "Number must be an integer between 1 and 20."}, 400

        add_to_history(request)

        recent_requests = app_history[-number:]
        return recent_requests[::-1], 200


@app.get("/current_age")
def current_age():
    """Returns a current age in years based on a given birthdate."""
    birthdate = request.args.get("date")

    if not isinstance(birthdate, str):
        return {
            "error": "Value for date parameter is invalid."
        }, 400

    try:
        date_format = datetime.strptime(birthdate, "%Y-%m-%d")
    except ValueError:
        return {
            "error": "Value for date parameter is invalid."
        }, 400

    return {"current_age": get_current_age(date_format.date())}, 200


if __name__ == "__main__":
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.run(port=8080, debug=True)
