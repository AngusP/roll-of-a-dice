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
    baseurl = sys.argv[1]
    apikey = sys.argv[2]
except Exception:
    print("Need two arguments, first is base URL for server and second is API key")
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


if __name__ == '__main__':
    # Register a login
    hostname = os.uname().nodename.partition('.')[0]
    username = os.getlogin()
    reg_login(apikey, username, hostname, '127.0.0.1')

