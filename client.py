#!/bin/env python

# ------------------------------------
#
#    R O L L    O F    A    D I C E
#
# ------------------------------------

import os
import requests

def reg_login(authkey, user, machine, addr):
    data = {
        'user'    : user,
        'machine' : machine,
        'address' : addr,
        'authkey' : authkey
    }
    response = requests.post('http://localhost:5000/hello', data)

apikey = os.environ.get('ROAD_API_KEY', '')

if __name__ == '__main__':
    # Register a login
    reg_login(apikey, 's1311631', 'TODO: Change me', '10.0.0.1')

