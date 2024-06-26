from id_dates import IdDates
from utils import connection

import config
import datetime
import json


def refresh():

    url = f"https://www.strava.com/api/v3/oauth/token?client_id={config.strava_client_id}&client_secret={config.strava_client_secret}&refresh_token={config.strava_refresh_token}&grant_type=refresh_token"

    resp = connection("POST", url)

    print(resp)

    config.strava_access_token = resp["access_token"]
    config.strava_refresh_token = resp["refresh_token"]
    

def get_activities(ebird_start_date: datetime) -> list:

    url = f"https://www.strava.com/api/v3/activities?access_token={config.strava_access_token}&per_page=5&page=1"

    resp = connection("GET", url)

    activity_list = __create_activity_list(resp, ebird_start_date)
    
    return activity_list


def update_activity(id: str, bird_list: str):
    
    print(bird_list)


def __create_activity_list(activities: json, ebird_start_date: datetime):
    
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


def __calculate_end_time(start_date, elapsed_time):

    delta = datetime.timedelta(seconds=elapsed_time)
    end_date = start_date + delta
    
    return end_date



