from channels.routing import ProtocolTypeRouter, URLRouter

from apps.games.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        websocket_urlpatterns,
    ),
})
