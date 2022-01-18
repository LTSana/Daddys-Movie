"""
ASGI config for DaddysMovie project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter, get_default_application
from channels.auth import AuthMiddlewareStack
import movie.routing

application = get_default_application()

route_application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            movie.routing.websocket_urlpatterns
        )
    ),
})
