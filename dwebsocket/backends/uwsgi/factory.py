
from dwebsocket.factory import WebSocketFactory
from .websocket import WebSocket

class uWsgiWebSocketFactory(WebSocketFactory): 

    def create_websocket(self):
        return WebSocket(self.request)