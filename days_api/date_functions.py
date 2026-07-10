"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Converts string to datetime object."""
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError as err:
        raise ValueError("Unable to convert value to datetime.") from err


def get_days_between(first: datetime, last: datetime) -> int:
    """Returns the number of days between two datetimes."""
    if not isinstance(first, datetime) or not isinstance(last, datetime):
        raise TypeError("Datetimes required.")
    delta = last-first
    return delta.days


def get_day_of_week_on(date_val: datetime) -> str:
    """Returns the day of the week of a specific datetime."""
    if not isinstance(date_val, datetime):
        raise TypeError("Datetime required.")
    weekdays = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]
    return weekdays[date_val.weekday()]


def get_current_age(birthdate: date) -> int:
    """Returns age in years."""
    if not isinstance(birthdate, date):
        raise TypeError("Date required.")

    age = date.today().year - birthdate.year

    if date.today().month < birthdate.month:
        age -= 1

    elif date.today().month == birthdate.month:
        if date.today().day < birthdate.day:
            age -= 1

    return age
