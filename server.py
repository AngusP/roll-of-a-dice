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
        self.r = redis.StrictRedis(decode_responses=True, 
                                   unix_socket_path='/tmp/roll-of-a-dice-redis.sock')
        self.keys_key = '__api_keys'
        self.log_k = '__log'

    def login(self, name, time):
        '''
        Log a login
        '''
        self._log(name, 'in{}', int(time))

    def logout(self, name, time):
        '''
        Log a logout
        '''
        self._log(name, 'out{}', int(time))

    def _log(self, name, time_fmt, time):
        '''
        Common between login and logout
        '''
        name = name.replace(':', '')
        time_s = time_fmt.format(time)
        self.r.zadd(self.log_k, time, '{}:{}'.format(name, time_s))
        self.r.lpush(name, time_s)


    def get_activity(self, time_start=0, time_end=-1):
        '''
        Return a range of log entries (raw)
        '''
        return [(x.strip(str(int(y))), str(int(y))) for x,y in \
                self.r.zrange(self.log_k, time_start, time_end, withscores=True)]


    def iter_activity(self):
        '''
        Iterate over log with Redis' SCAN guarantees but cleaner data
        '''
        for name, stamp in self.r.zscan_iter(self.log_k, score_fast_func=int):
            yield name.strip(str(stamp)), stamp


    def gen_key(self):
        '''
        Generate and return an API key
        '''
        rand = ''.join( [chr(random.randint(48,122)) for i in range(0,32)] )
        rand.replace('\\', '_') # remove pesky escapes
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
        return self.r.zrange(self.keys_key, 0, -1)



api = Flask(__name__)
utils = ServerUtils()

@api.route('/hello', methods=['POST'])
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
    _log_event(request, 'login')


@api.route('/bye', methods=['POST'])
def bye():
    '''
    Register logout on a machine, echo back to user.
    
    Post:
    -----

    user     --  Username on machine
    authkey  --  Authorised API key
    machine  --  Human readable name of machine
    address  --  IP Address of machine (not validated)
    '''
    _log_event(request, 'logout')



def _log_event(request, event_type)
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
            'error' : 'Not Authorised, bad key {}'.format(key),
            'code'  : 401
        }), 401

    if event_type == 'login':
        utils.login(machine, time)
    elif event_type == 'logout':
        utils.logout(machine, time)
        

    # TODO: Do something with user and address data

    return json.dumps({
        'machine' : machine,
        'time'    : time,
        'address' : address,
        'user'    : user,
        'code'    : 200
    })


@api.route('/activity')
def activity():
    try:
        key     = request.args['authkey']
    except KeyError:
        return json.dumps({
            'error' : 'Missing GET data',
            'code'  : 400
        }), 400
    return json.dumps(utils.get_activity())


if __name__ == '__main__':
    if 'develop' not in sys.argv:
        api.run(host='0.0.0.0', port='80')
    elif 'interactive' not in sys.argv:
        api.run(host='0.0.0.0', port='5000')
        

