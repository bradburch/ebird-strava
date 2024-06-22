import config
import ebird


def main():
    bird_list = ebird.build_list(config.profile_id)
    print(bird_list)
    

if __name__ == "__main__":
    main()
