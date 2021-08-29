import socket
import sys
import requests

from asylum import config
from asylum.asylumd import jsonrpc

def sendToServer(request):
    try:
        return requests.get(config['SUBSYSTEMS']['iotchief_url']+"arduino/"+request, timeout=1).json()
    except (requests.exceptions.RequestException, ValueError) as e:
        return e

def ping():
    req = "ping"
    print(sendToServer(req))

def shutterAction(id, action):
    if id < 0 or id > 8 or action < 0 or action > 2:
        return
    req = "shutter?id={}&action={}".format(id, action)
    print(sendToServer(req))

def main():
    if len(sys.argv) < 2:
            print("asylum_client.py ping")
            print("asylum_client.py shutter [id] [action]")
            sys.exit(1)

    if sys.argv[1] == 'ping':
        ping()
    elif sys.argv[1] == "shutter":
        id = int(sys.argv[2])
        action = int(sys.argv[3])
        shutterAction(id, action)

if __name__ == '__main__':
    main()
