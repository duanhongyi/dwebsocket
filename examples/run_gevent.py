import sys
import getopt
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer
from examples.wsgi import application


addr, port = '127.0.0.1', 8000
opts, _ = getopt.getopt(sys.argv[1:], "b:")
for opt, value in opts:
    if opt == '-b':
        addr, port = value.split(":")
server = WSGIServer((addr, int(port)), application)
server.serve_forever()
