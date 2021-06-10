from django.urls import path

from .consumer import ChatConsumer, MovieStatusConsumer

websocket_urlpatterns = [
    path("ws/chat/<slug:sessionID>/", ChatConsumer.as_asgi()),
    path("ws/movie/<slug:sessionID>/", MovieStatusConsumer.as_asgi()),
]
