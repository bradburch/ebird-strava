import json
import requests
import string

def connection(url: string, headers={}, data={}) -> json: 
    response = requests.get(url, headers=headers, data=data)

    return response.json()
