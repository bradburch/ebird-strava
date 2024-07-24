from id_dates import IdDates
from utils import connection

import config
import datetime
import json


def refresh() -> None:

    path = "oauth/token"
    params = {
        "client_id": config.strava_client_id,
        "client_secret": config.strava_client_secret,
        "refresh_token": config.strava_refresh_token,
        "grant_type": "refresh_token"
    }

    url = __create_url(path, params)
    resp = connection("POST", url)
    respJson = resp.json()

    config.strava_access_token = respJson["access_token"]
    config.strava_refresh_token = respJson["refresh_token"]


def get_activities(ebird_start_date: datetime) -> list:

    path = "activities"
    params = {
        "access_token": config.strava_access_token,
        "per_page": "5",
        "page": "1",
    }

    url = __create_url(path, params)
    resp = connection("GET", url)
    respJson = resp.json()

    activity_list = __create_activity_list(respJson, ebird_start_date)
    
    return activity_list


def update_activity(id: str, bird_list: str) -> json:

    title = "Birds seen during activity:"
    description = f"{title}\n" + bird_list
    
    data = {
        "description": description
    }

    path = "activities"
    params = {
        "access_token": config.strava_access_token,
    }

    url = __create_url(path, params, id)
    resp = connection("PUT", url, data=data)
    
    return resp


def __create_activity_list(activities: json, ebird_start_date: datetime) -> list:
    
    activity_list = []

    for i in range(len(activities)):
        activity = activities[i]

        start_date_local = activity["start_date_local"]
        strava_start_date = datetime.datetime.fromisoformat(start_date_local)

        if strava_start_date.date() == ebird_start_date.date():
            id = activity["id"]
            elapsed_time = activity["elapsed_time"]
            end_date = __calculate_end_time(strava_start_date, elapsed_time)
            act = IdDates(id, strava_start_date, end_date)
  
            activity_list.append(act)

    return activity_list


def __calculate_end_time(start_date, elapsed_time) -> datetime:

    delta = datetime.timedelta(seconds=elapsed_time)
    end_date = start_date + delta
    
    return end_date


def __create_url(path: str, params: dict, id: str = None) -> str:

    strava_api_url = "https://www.strava.com/api/v3/"
    params_list = "&".join("{}={}".format(key, value) for key, value in params.items())

    url = f"{strava_api_url}{path}?"
    if id: 
        url = f"{url}{id}{params_list}"
    else:
        url = f"{url}{params_list}"

    return url
