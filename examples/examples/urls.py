import threading
from django.conf.urls import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from dwebsocket.decorators import accept_websocket

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

def base_view(request):
    return render_to_response('index.html', {

    }, context_instance=RequestContext(request))


clients = []

@accept_websocket
def echo(request):
    if request.is_websocket:
        lock = threading.RLock()
        try:
            lock.acquire()
            clients.append(request.websocket)
            for message in request.websocket:
                if not message:
                    break
                for client in clients:
                    client.send(message)
        finally:
            clients.remove(request.websocket)
            lock.release()


urlpatterns = patterns('',
    # Example:
    url(r'^$', base_view),
    url(r'^echo$', echo),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
