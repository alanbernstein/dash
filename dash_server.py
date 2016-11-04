#!/usr/bin/python
# enable debugging
import os
import sys
import socket
import pwd
import cgi
import cgitb
import urlparse
from pprint import pprint
from time import strftime, localtime, time

# dash.py?press=stove
# dash.py?last=stove
#
cgitb.enable(format='text')
print "Content-Type: text/plain;charset=utf-8"
print

data_path = '/home/alanb0/public_html/data/dash/'
max_records = 10  # not implemented

def main():
    req_time = time()
    env = os.environ
    url = env['REQUEST_URI']
    params = urlparse.parse_qs(urlparse.urlparse(url).query)

    if 'press' in params:
        button = params['press'][0]
        handle_button_press(env, button, req_time)
    elif 'last' in params:
        button = params['last'][0]
        get_last_record(env, button, req_time)
    else:
        print('?')
    # todo: handle different types of display requests
    # - total count
    # - count in time period
    # - etc


def handle_button_press(env, button, req_time):
    addr = env['REMOTE_ADDR']
    port = env['REMOTE_PORT']
    
    fname = data_path + button + '.txt'
    try:
        with open(fname, 'a') as f:
            f.write('%s %s %s\n' % (req_time, addr, port))
    except Exception as e:
        print('error %s' % e)
    else:
        print('success %s' % req_time)


def get_last_record(env, button, req_time):
    fname = data_path + button + '.txt'
    with open(fname, 'r') as f:
        for line in f:
            pass

    print(line.split(' ')[0])


if __name__=='__main__':
    main()
