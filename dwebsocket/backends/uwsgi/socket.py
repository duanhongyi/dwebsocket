import uwsgi


class Socket(object):

    def __init__(self, request):
        self.request = request


    def fileno(self):
        return self.request.META["wsgi.input"].fileno()

    def recv(self, bufsize):
        uwsgi.wait_fd_read(self.fileno(), 300)
        uwsgi.suspend()
        return uwsgi.recv(self.fileno(), bufsize)

    def send(self, body):
        return uwsgi.send(self.fileno(), body)

    def close(self):
        uwsgi.close(self.fileno())