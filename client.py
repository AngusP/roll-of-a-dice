#!/bin/env python

# ------------------------------------
#
#    R O L L    O F    A    D I C E
#
# ------------------------------------

import os
import sys
import requests

try:
    req_type = sys.argv[1]
    baseurl = sys.argv[2]
    apikey = sys.argv[3]
except Exception:
    print("Need three arguments, first is the request type,"
    "second is base URL for server and third is API key")
    sys.exit(-1)
    raise

def reg_login(authkey, user, machine, addr):
    data = {
        'user'    : user,
        'machine' : machine,
        'address' : addr,
        'authkey' : authkey
    }
    response = requests.post(baseurl + '/hello', data)
    response.raise_for_status()


def reg_logout(authkey, user, machine, addr):
    data = {
        'user'    : user,
        'machine' : machine,
        'address' : addr,
        'authkey' : authkey
    }
    response = requests.post(baseurl + '/bye', data)
    response.raise_for_status()


def get_activity():
    raise NotImplementedError()


if __name__ == '__main__':
    # Register a login
    hostname = os.uname().nodename.partition('.')[0]
    username = os.getlogin()
    # TODO: IP Address

    if req_type == 'login':
        reg_login(apikey, username, hostname, '127.0.0.1')

    elif req_type == 'logout':
        reg_logout(apikey, username, hostname, '127.0.0.1')

    elif req_type == 'activity':
        print(get_activity())

