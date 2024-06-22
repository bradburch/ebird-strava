import config
import string
import utils

import json

_ebird_api_header = {
    'X-eBirdApiToken': config.ebird_api_token
    }


def build_list(username: string): 

    sub_id = __get_recent_checklist(username)
    observations = __get_observations(sub_id)
    code_num = parse(observations, "speciesCode", "howManyStr")
    taxonomy = __get_taxonomy(code_num)
    code_species = parse(taxonomy, "speciesCode", "comName")
    species_num = __combine_species_num(code_num, code_species)
    return __create_bird_list(species_num)


def __get_recent_checklist(username: string) -> string: 
    
    url = f"https://ebird.org/prof/lists?username={username}==&r=world"

    resp = utils.connection(url)

    sub_id = resp[0]["subId"]

    return sub_id


def __get_observations(sub_id: string) -> dict:

    url = f"https://api.ebird.org/v2/product/checklist/view/{sub_id}"

    resp = utils.connection(url, _ebird_api_header)

    return resp["obs"]


def __get_taxonomy(code_num: dict): 
    
    codes = "".join("&species=" + key for key, _ in code_num.items())

    url = f"https://api.ebird.org/v2/ref/taxonomy/ebird?{codes}&fmt=json"

    return utils.connection(url, _ebird_api_header)


def __combine_species_num(code_num: dict, code_species: dict) -> dict:
     
    species_num = {}
     
    for key, value in code_num.items():
        species_num[code_species[key]] = value
    
    return species_num


def __create_bird_list(species_num: dict) -> string:

    bird_list = " ".join(value + " " + key + "\n" for key, value in species_num.items())

    return bird_list
    

def parse(response: list, key1: string, key2: string) -> dict:
    
    new_dict = {}

    for i in range(len(response)):
        new_dict[response[i][key1]] = response[i][key2]

    return new_dict
