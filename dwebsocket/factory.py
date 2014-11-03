import logging
import socket
from .websocket import WebSocket
from .protocols import get_websocket_protocol


logger = logging.getLogger(__name__)


class WebSocketFactory(object): 
    def __init__(self, request):
        self.request = request

    def is_websocket(self):
        """check the websocket"""
        if self.request.META.get(
            'HTTP_UPGRADE', ""
        ).lower() == 'websocket':
            return True
        else:
            return False

    def get_websocket_version(self):
        if 'HTTP_SEC_WEBSOCKET_KEY1' in self.request.META:
            protocol_version = '76'
            if 'HTTP_SEC_WEBSOCKET_KEY2' not in self.request.META:
                raise ValueError('HTTP_SEC_WEBSOCKET_KEY2 NOT FOUND')
        elif 'HTTP_SEC_WEBSOCKET_KEY' in self.request.META:
            protocol_version = '13'
        else:
            protocol_version = '75'
        return protocol_version

    def get_wsgi_sock(self):
        if 'gunicorn.socket' in self.request.META:
            sock = self.request.META['gunicorn.socket'].dup()
        else:
            wsgi_input = self.request.META['wsgi.input']
            if hasattr(wsgi_input, '_sock'):
                sock = wsgi_input._sock
            elif hasattr(wsgi_input, 'rfile'):  # gevent
                sock = wsgi_input.rfile._sock
            else:
                raise ValueError('Socket not found in wsgi.input')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        return sock

    def create_websocket(self):
        if not self.is_websocket():
            return None
        try:
            protocol = get_websocket_protocol(self.get_websocket_version())(
                sock = self.get_wsgi_sock(),
                headers = self.request.META
            )
            return WebSocket(protocol=protocol)
        except KeyError as e:
            logger.exception(e)
        return None
