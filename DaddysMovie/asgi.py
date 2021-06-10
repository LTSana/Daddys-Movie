"""
ASGI config for DaddysMovie project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Channel Security
from channels.security.websocket import AllowedHostsOriginValidator

import movie.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DaddysMovie.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                movie.routing.websocket_urlpatterns
            )
        )
    ),
}) 