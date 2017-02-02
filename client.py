#!/bin/env python

# ------------------------------------
#
#    R O L L    O F    A    D I C E
#
# ------------------------------------

import os
import requests

if __name__ == '__main__':
    # Register a login
    data = {
        'user'    : 's1311631',
        'machine' : 'TODO: Change me',
        'address' : '10.0.0.1',
        'authkey' : os.environ.get('ROAD_API_KEY', '')
    }
    response = requests.post('http://localhost:5000/hello', data)

