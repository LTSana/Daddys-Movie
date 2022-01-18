"""
ASGI config for DaddysMovie project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DaddysMovie.settings")

import django
django.setup()

from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DaddysMovie.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
django_asgi_app = get_asgi_application()

import movie.routing


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            movie.routing.websocket_urlpatterns
        )
    ),
})