import json
import requests
import string

def connection(method: string, url: string, headers={}, data={}) -> json: 
    response = requests.request(method, url, headers=headers, data=data)

    return response.json()
