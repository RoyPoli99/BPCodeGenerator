import http
import urllib
import json
from http.client import BadStatusLine

import requests

URL = "http://localhost:8080"


def send_request(message):
    # http = urllib3.PoolManager()
    # response = http.request('POST', URL, body=message.encode('utf8'))
    # return response.read().encode('utf8')
    msg = message.encode('utf8')
    req = urllib.request.Request(URL, data=message.encode('utf8'), headers={})
    try:
        response = urllib.request.urlopen(req)
    except http.client.HTTPException as e:
        return e
    return response.read().decode('utf8')


def calculate_fitness(instance):
    y = send_request(instance)
    x = y.line
    return float(x)
