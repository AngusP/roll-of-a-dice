#!/bin/env python

# ------------------------------------
#
#    R O L L    O F    A    D I C E
#
# ------------------------------------

import redis
import json
import random
import sys
from flask import Flask, request
from time import time as unix_time

class ServerUtils(object):

    def __init__(self):
        self.r = redis.StrictRedis(decode_responses=True)
        self.keys_key = '__api_keys'
        self.login_k = 'logins'

    def login(self, name, time):
        '''
        Log a login
        '''
        self.r.zadd(self.login_k, int(time), name)

    def get_logins(self, time_start=0, time_end=-1):
        '''
        Return a range of logins
        '''
        return self.zrange(self.login_k, time_start, time_end, withscores=True)


    def gen_key(self):
        '''
        Generate and return an API key
        '''
        rand = ''.join( [chr(random.randint(33,126)) for i in range(0,32)] )
        self._add_key(rand)
        return rand

    def _add_key(self, key):
        '''
        Add a new API key
        '''
        return self.r.zadd(self.keys_key, int(unix_time()), key)

    def validate_key(self, key):
        '''
        Check if key exists, touch it if so
        '''
        if self.r.zscore(self.keys_key, key) is not None:
            # Update 'touched' score
            self.r.zadd(self.keys_key, int(unix_time()), key)
            return True
        return False

    def get_keys(self):
        '''
        List API keys. Score is 'last used' timestamp
        '''
        return self.zrange(self.keys_key, 0, -1)



api = Flask(__name__)
utils = ServerUtils()

@api.route("/hello", methods=['POST'])
def hello():
    '''
    Register login on a machine, echo back to user.
    
    Post:
    -----

    user     --  Username on machine
    authkey  --  Authorised API key
    machine  --  Human readable name of machine
    address  --  IP Address of machine (not validated)
    '''
    try:
        time    = int(unix_time())
        key     = request.form['authkey']
        user    = request.form['user']
        machine = request.form['machine']
        address = request.form['address']
    except KeyError:
        return json.dumps({
            'error' : 'Missing POST data',
            'code'  : 400
        }), 400
    
    if not utils.validate_key(key):
        return json.dumps({
            'error' : 'Not Authorised',
            'code'  : 401
        }), 401

    # Record login
    utils.login(machine, time)

    # TODO: Do something with user and address data

    return json.dumps({
        'machine' : machine,
        'time'    : time,
        'address' : address,
        'user'    : user
    })



if __name__ == '__main__' and 'debug' not in sys.argv:
        api.run()

