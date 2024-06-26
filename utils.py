from id_dates import IdDates
import json
from requests import request


def connection(method: str, url: str, headers={}, data={}) -> json: 
    response = request(method, url, headers=headers, data=data)

    return response.json()


def compare(strava: IdDates, ebird: IdDates) -> bool:

    latest_start = max(strava.start_date, ebird.start_date)
    earliest_end = min(strava.end_date, ebird.end_date)
    delta = (earliest_end - latest_start).days + 1

    return delta > 0