import config

from ebird import build_list, get_ebird_dates_observation, get_recent_checklist
from strava import get_activities, refresh, update_activity
from utils import compare


def main():

    ebird_start_date, ebird_id = get_recent_checklist(config.profile_id)
    refresh()
    activity_list = get_activities(ebird_start_date)

    if activity_list:
        ebird_dates, observation = get_ebird_dates_observation(ebird_id, ebird_start_date)

        for i in range(len(activity_list)):
            if compare(activity_list[i], ebird_dates): 
                ebird_list = build_list(observation)
                update_activity(activity_list[i].id, ebird_list)
        

if __name__ == "__main__":
    main()
