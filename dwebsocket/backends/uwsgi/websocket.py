import uwsgi
import collections
from dwebsocket import websocket


class WebSocket(websocket.WebSocket):
    """
    A websocket object that handles the details of
    serialization/deserialization to the socket.

    The primary way to interact with a :class:`WebSocket` object is to
    call :meth:`send` and :meth:`wait` in order to pass messages back
    and forth with the browser.
    """

    def __init__(self, request):
        self.request = request
        self.closed = False
        self._message_queue = collections.deque()

    def accept_connection(self):
        uwsgi.websocket_handshake(
            self.request.META['HTTP_SEC_WEBSOCKET_KEY'],
            self.request.META.get('HTTP_ORIGIN', '')
        )

    def _get_new_messages(self):
        while True:
            message = uwsgi.websocket_recv_nb()
            if not message:
                break
            else:
                self._message_queue.append(message)

    def send(self, message):
        '''
        Send a message to the client. *message* should be convertable to a
        string; unicode objects should be encodable as utf-8.
        '''
        try:
            uwsgi.websocket_send(message)
        except IOError:
            self.close()

    def count_messages(self):
        '''
        Returns the number of queued messages.
        '''
        self._get_new_messages()
        return len(self._message_queue)

    def has_messages(self):
        '''
        Returns ``True`` if new messages from the socket are available, else
        ``False``.
        '''
        if self._message_queue:
            return True
        self._get_new_messages()
        if self._message_queue:
            return True
        return False

    def read(self, fallback=None):
        '''
        Return new message or ``fallback`` if no message is available.
        '''
        if self.closed:
            return None
        if self.has_messages():
            return self._message_queue.popleft()
        return fallback

    def wait(self):
        '''
        Waits for and deserializes messages. Returns a single message; the
        oldest not yet processed.
        '''
        if self.closed:
            return None
        if not self._message_queue:
            message = uwsgi.websocket_recv()
            if not message:
                return message
            self._message_queue.append(message)
        return self._message_queue.popleft()

    def close(self, code=None, reason=None):
        '''
        Forcibly close the websocket.
        '''
        self.closed = True