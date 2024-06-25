import config
import utils
import activity

import json
import string


def get_auth(): 

    # url = f"https://www.strava.com/api/v3/oauth/token?client_id=${config.strava_client_id}&client_secret={config.strava_client_secret}&code={config.strava_code}&grant_type=authorization_code"
    get_activities()
    # print(utils.connection("POST", url))

def get_activities():

    url = f"https://www.strava.com/api/v3/activities?access_token={config.strava_access_token}&per_page=5&page=1"

    activities = utils.connection("GET", url)

    activity_list = []

    for i in range(len(activities)):
        activity = activities[i]

        print(activity["id"])
        print(activity["elapsed_time"])
        print(activity["start_date_local"])