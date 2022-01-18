from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.auth import AuthMiddlewareStack
import movie.routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            movie.routing.websocket_urlpatterns
        )
    ),
})