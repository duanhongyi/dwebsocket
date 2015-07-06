import uwsgi
from dwebsocket.backends.default.factory import WebSocketFactory
from dwebsocket.backends.default.protocols import get_websocket_protocol
from .socket import Socket
from .websocket import WebSocket


class uWsgiWebSocketFactory(WebSocketFactory): 

    def get_wsgi_sock(self):
        return Socket(self.request)