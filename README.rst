================
dwebsocket
================

The **dwebsocket** module provides an implementation of the WebSocket
Protocol for django. 

This module implements the final version of the WebSocket protocol as
defined in `RFC 6455 <http://tools.ietf.org/html/rfc6455>`_.  Certain
browser versions (notably Safari 5.x) implemented an earlier draft of
the protocol (known as "draft 76") and are not compatible with this module.

The **dwebsocket** module based django-websocket development, django-websocket
module in `https://github.com/gregmuellegger/django-websocket`.
Thank you Gregor Müllegger.

Usage
=====

You can use the ``accept_websocket`` decorator if you want to handle websocket
connections just for a single view - it will route standard HTTP requests to
the view as well. Use ``require_websocket`` to only allow WebSocket
connections but reject normal HTTP requests.

You can use a middleware if you want to have WebSockets available for *all*
URLs in your application. Add
``dwebsocket.middleware.WebSocketMiddleware`` to your
``MIDDLEWARE_CLASSES`` setting. This will still reject websockets for normal
views. You have to set the ``accept_websocket`` attribute on a view to allow
websockets.

To allow websockets for *every single view*, set the ``WEBSOCKET_ACCEPT_ALL``
setting to ``True``.

The request objects passed to a view, decorated with ``accept_websocket`` or
``require_websocket`` will have the following attributes/methods attached.
These attributes are always available if you use the middleware.

``request.is_websocket()``
--------------------------

Returns either ``True`` if the request has a valid websocket or ``False`` if
its a normal HTTP request. Use this method in views that can accept both types
of requests to distinguish between them.

``request.websocket``
---------------------

After a websocket is established, the request will have a ``websocket``
attribute which provides a simple API to communicate with the client. This
attribute will be ``None`` if ``request.is_websocket()`` returns ``False``.

It has the following public methods:

``WebSocket.wait(timeout=-1)``
~~~~~~~~~~~~~~~~~~~~

This will return exactly one message sent by the client. It will not return
before a message is received or the conection is closed by the client. In this
case the method will return ``None``.

``WebSocket.read()``
~~~~~~~~~~~~~~~~~~~~

The ``read`` method will return either a new message if available or ``None``
if no new message was received from the client. It is a non-blocking
alternative to the ``wait()`` method.

``WebSocket.count_messages()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the number of queued messages.

``WebSocket.has_messages()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns ``True`` if new messages are available, else ``False``.

``WebSocket.send(message)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will send a single message to the client.

``WebSocket.__iter__()``
~~~~~~~~~~~~~~~~~~~~~~~~

You can use the websocket as iterator. It will yield every new message sent by
the client and stop iteration after the client has closed the connection.

``WebSocket.is_closed()``
~~~~~~~~~~~~~~~~~~~~~~~~
Return to ``True`` if websocket is closed, else ``False``.

Error handling
--------------

The library will return a Http 400 error (Bad Request) if the client requests
a WebSocket connection, but the request is malformed or not supported by
*dwebsocket*.

Examples
========

Receive one message from the client, send that message back to the client and
close the connection (by returning from the view)::

    from dwebsocket import require_websocket

    @require_websocket
    def echo_once(request):
        message = request.websocket.wait()
        request.websocket.send(message)

Send websocket messages from the client as lowercase and provide same
functionallity for normal GET requests::

    from django.http import HttpResponse
    from dwebsocket import accept_websocket

    def modify_message(message):
        return message.lower()

    @accept_websocket
    def lower_case(request):
        if not request.is_websocket():
            message = request.GET['message']
            message = modify_message(message)
            return HttpResponse(message)
        else:
            for message in request.websocket:
                message = modify_message(message)
                request.websocket.send(message)


Change websocket backends
-------------------

Currently supports two kinds of backends, they are default and uwsgi.

Django develop server, eventlent, gevent, gunicore are supported by default.

If you want to use the uwsgi backend, add `WEBSOCKET_FACTORY_CLASS` in the settings.py file::

    WEBSOCKET_FACTORY_CLASS = 'dwebsocket.backends.uwsgi.factory.uWsgiWebSocketFactory'

Run uwsgi::

    uwsgi --http :8080 --http-websockets --processes 1 \
    --wsgi-file wsgi.py--async 30 --ugreen --http-timeout 300


Using in production
-------------------

Currently there is a cluster of two machines being used dwebsocket, it uses
gevent wsgi deployed, each machine around 150,000 concurrent connections.


Contribute
==========

Every contribution in any form is welcome. Ask questions, report bugs, request
new features, make rants or tell me any other critique you may have.

One of the biggest contributions you can make is giving me a quick *Thank you*
if you like this library or if it has saved you a bunch of time.

But if you want to get your hands dirty:

- Get the code from github: https://github.com/duanhongyi/dwebsocket
- Start coding :)
- Send me a pull request or an email with a patch.
