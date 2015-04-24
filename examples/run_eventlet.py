from eventlet import wsgi, patcher
patcher.monkey_patch()

import sys
import getopt
import eventlet
from examples.wsgi import application


addr, port = '127.0.0.1', 8000
opts, _ = getopt.getopt(sys.argv[1:], "b:")
for opt, value in opts:
    if opt == '-b':
        addr, port = value.split(":")

wsgi.server(eventlet.listen((addr, int(port))), application)
