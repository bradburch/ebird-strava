import config
import ebird
import strava


def main():
    # bird_list = ebird.build_list(config.profile_id)
    # print(bird_list)
    strava.get_activities()

    

if __name__ == "__main__":
    main()
