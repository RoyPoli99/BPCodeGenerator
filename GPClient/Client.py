import urllib.request
import json

URL = "TBD"


def send_request(message):
    app_json = json.dumps(message).encode('utf8')

    req = urllib.request.Request(URL, data=app_json, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)

    return response.read().decode('utf8')


def calculate_fitness(instance):
    return float(send_request(instance))
