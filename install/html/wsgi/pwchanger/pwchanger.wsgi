"""
This wsgi file depends on a certain layout:

pwchanger.wsgi
pwchanger/service.py  (and the rest)

"""
import sys
import logging
import site
import os
import pprint

MAIN_APP_PATH = os.path.dirname(os.path.realpath(__file__))
MAIN_APP_PATH = os.path.join(MAIN_APP_PATH,'pwchanger')
sys.path.append(MAIN_APP_PATH)

from service import create_app

# Python's bundled WSGI server
from wsgiref.simple_server import make_server

def application (environ, start_response):
    print ("app called")
    print ("sd:{}".format(MAIN_APP_PATH))
    app = create_app()

    r = app.__call__(environ,start_response)

    return r
