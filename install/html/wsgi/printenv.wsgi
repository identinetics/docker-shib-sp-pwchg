#! /var/www/wsgi/venv python

import sys


# Python's bundled WSGI server
from wsgiref.simple_server import make_server

def application (environ, start_response):

    lines = [
         'python version: {}\n'.format(sys.version),
         'pyenv: {}\n'.format(sys.prefix)
    ]

    # Sorting and stringifying the environment key, value pairs
    e = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
   
    lines += e 
    response_body = '\n'.join(lines)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)

    resp_b = str.encode(response_body)

    return [resp_b]
