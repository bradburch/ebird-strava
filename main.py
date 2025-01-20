from ebird import build_bird_dict, create_bird_description, get_ebird_dates_observation, get_recent_checklists
from strava import get_recent_activities, refresh, update_activity
from utils import add_dict, compare


def main():

    ebird_start_date = get_recent_checklists()
    refresh()
    activity_list = get_recent_activities()

    ebird_checklists_with_activities = list(filter(lambda x: activity_list.get(x.start_date.date()) != None, ebird_start_date))

    if ebird_checklists_with_activities:
        activity_species = {}

        for checklist in ebird_checklists_with_activities: 
            end_date, observation = get_ebird_dates_observation(checklist)
            checklist.update_end_date(end_date)
            checklist.update_obs(observation)

            activity = activity_list.get(checklist.start_date.date())
            activity_id = activity.identifier

            if compare(activity, checklist):
                bird_dict = build_bird_dict(checklist.obs)
                if activity_id in activity_species:
                    activity_species[activity_id] = add_dict(activity_species[activity_id], bird_dict)
                else:
                    activity_species[activity_id] = bird_dict

        for k, v in activity_species.items():
            birds = create_bird_description(v)
            print(birds)
            resp = update_activity(k, birds)

            if resp.status_code == 200:
                print(f"Updated Strava activity {k}")
            else:
                print(f"Unable to update activity {k}")

    else:
        print("No matching Strava activities and eBird checklists!")


if __name__ == "__main__":
    main()
