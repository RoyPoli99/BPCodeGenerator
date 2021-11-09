import http
import urllib
import json
from http.client import BadStatusLine
import bp_pb2
import socket
import google.protobuf.service
import ProtoClient

URL = "http://localhost:8081"
TCP_IP = '127.0.0.1'
TCP_PORT = 8081
BUFFER_SIZE = 1024
pc = ProtoClient.ProtoClient()


def send_proto_request(individual):
    response = pc.get_url(individual)
    return response


def send_request(message):
    msg = message.SerializeToString()

    # req = urllib.request.Request(URL, data=msg, headers={})
    # try:
    #     response = urllib.request.urlopen(req)
    # except http.client.HTTPException as e:
    #     return e
    # return response.read().decode('utf8')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(msg)
    # s.send(bytes(1))
    data = s.recv(BUFFER_SIZE)
    s.close()
    return data


def calculate_fitness(instance):
    y = send_request(instance)
    x = y.line
    return float(x)


def send_stop():
    message = "STOP_SERVER"
    req = urllib.request.Request(URL, data=message.encode('utf8'), headers={})
    try:
        urllib.request.urlopen(req)
    except http.client.HTTPException as e:
        return