from id_dates import IdDates

from datetime import datetime, timezone, timedelta
from utils import connection

import config
import json

_ebird_api_header = {
    'X-eBirdApiToken': config.ebird_api_token
    }


def build_bird_dict(observation: json) -> dict:

    code_num = parse(observation, "speciesCode", "howManyStr")
    taxonomy = __get_taxonomy(code_num)
    code_species = parse(taxonomy, "speciesCode", "comName")
    species_num = __combine_species_num(code_num, code_species)
    
    return species_num


def get_recent_checklists(username: str) -> dict: 
    
    ebird_url = "https://ebird.org"

    path = "/prof/lists"
    params = {
        "r": "world",
        "username": username
    }

    url = __create_url(path, params,ebird_api_url=ebird_url)
    resp = connection("GET", url)
    respJson = resp.json()

    start_id = __get_ids_and_starts(respJson)
    
    return start_id


def __get_ids_and_starts(respJson: json) -> dict:

    start_id = []

    for cl in respJson:
        iso_obs_date = cl["isoObsDate"]
        identifier = cl["subId"]
        start_date = datetime.fromisoformat(iso_obs_date)
        start_date_local = start_date.replace(tzinfo=timezone.utc)
        idDate = IdDates(identifier, start_date_local)

        start_id.append(idDate)

    return start_id


def get_ebird_dates_observation(id_date: IdDates) -> tuple:

    identifier = id_date.identifier
    start_date = id_date.start_date

    observation = __get_observation(identifier)
    elapsed_time = observation["durationHrs"]
    end_date = __calculate_end_time(start_date, elapsed_time)

    return (end_date, observation["obs"])


def __get_observation(sub_id: str) -> dict:

    path = "product/checklist/view"
    params = {}

    url = __create_url(path, params, id=sub_id)
    resp = connection("GET", url, _ebird_api_header)

    return resp.json()


def __get_taxonomy(code_num: dict) -> dict: 
    
    codes = "".join("&species=" + key for key, _ in code_num.items())

    path = "ref/taxonomy/ebird"
    params = {
        "": codes,
        "fmt": "json"
    }

    url = __create_url(path, params)
    resp = connection("GET", url, _ebird_api_header)

    return resp.json()


def __combine_species_num(code_num: dict, code_species: dict) -> dict:
     
    species_num = {}
     
    for key, value in code_num.items():
        species_num[code_species[key]] = value
    
    return species_num


def create_bird_description(species_num: dict) -> str:

    bird_list = "".join(value + " " + key + "\n" for key, value in species_num.items())

    return bird_list


def parse(response: list, key1: str, key2: str) -> dict:

    new_dict = {}

    for i in range(len(response)):
        new_dict[response[i][key1]] = response[i][key2]

    return new_dict


def __calculate_end_time(start_date: datetime, elapsed_time: datetime) -> datetime:

    delta = timedelta(hours=elapsed_time)
    end_date = start_date + delta
    
    return end_date


def __create_url(path: str, params: dict, ebird_api_url: str = "https://api.ebird.org/v2/", id: str = None) -> str:
    
    params_list = "&".join("{}={}".format(key, value) for key, value in params.items())

    url = f"{ebird_api_url}{path}"

    if id:
        url = f"{url}/{id}"
    else:
        url = f"{url}?{params_list}"

    return url
