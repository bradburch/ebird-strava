import config
import ebird
import strava
import ebird_strava_compare


def main():
    ebird_start_date, ebird_id = ebird.get_recent_checklist(config.profile_id)
    strava.refresh()
    activity_list = strava.get_activities(ebird_start_date)

    if activity_list:
        ebird_dates, observation = ebird.get_observation(ebird_id, ebird_start_date)
        print(ebird_dates)
        print(observation)
        for i in range(len(activity_list)):
            if ebird_strava_compare.compare(activity_list[i], ebird_dates): 
                ebird_list = ebird.build_list(ebird_id)
                strava.update_activity(strava.id, ebird_list)
        

    

if __name__ == "__main__":
    main()
