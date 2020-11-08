import http
import urllib.request
import json
import requests

URL = "http://localhost:8080"


def send_request(message):
    app_json = json.dumps(message).encode('utf8')

    req = urllib.request.Request(URL, data=message.encode('utf8'))
    try:
        response = urllib.request.urlopen(req)
    except http.client.HTTPException as e:
        return e
    return response


def calculate_fitness(instance):
    return float(send_request(instance))
