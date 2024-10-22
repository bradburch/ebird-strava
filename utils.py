from id_dates import IdDates
import json
from requests import request


def connection(method: str, url: str, headers={}, data={}) -> json: 

    response = request(method, url, headers=headers, data=data)

    if response.status_code == 200:
        return response
    else:
        print('ERROR')
        print(response.json())
        return response


def compare(strava: IdDates, ebird: IdDates) -> bool:

    latest_start = max(strava.start_date, ebird.start_date)
    earliest_end = min(strava.end_date, ebird.end_date)
    delta = (earliest_end - latest_start).days + 1

    return delta > 0


def add_dict(current: dict, new: dict):

    new_dict = current.copy()

    for k, v in new.items():
        if k in new_dict:
            if v.isnumeric() and new_dict[k].isnumeric():
                new_value = int(v) + int(new_dict[k])
                new_dict[k] = str(new_value)
            elif not v.isnumeric() or not new_dict[k].isnumeric():
                new_dict[k] = 'X'
        else:
            new_dict[k] = v

    return new_dict
