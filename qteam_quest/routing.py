from channels.routing import ProtocolTypeRouter, URLRouter

import apps.games.routing

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        apps.games.routing.websocket_urlpatterns,
    ),
})
