import uwsgi


class Socket(object):

    def __init__(self, request):
        self.request = request
        self.closed = False


    def fileno(self):
        return self.request.META["wsgi.input"].fileno()

    def recv(self, bufsize):
        if not self.closed:
            uwsgi.wait_fd_read(self.fileno(), 300)
            uwsgi.suspend()
        if not self.closed:
            return uwsgi.recv(self.fileno(), bufsize)

    def send(self, body):
        if not self.closed:
            return uwsgi.send(self.fileno(), body)

    def close(self):
        self.closed = True
        uwsgi.close(self.fileno())