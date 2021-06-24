from django.urls import path

from . import views

urlpatterns = [
    path("fetch", views.fetchAllMessages, name="fetch_message"),
    path("send", views.newMessage, name="new_message_message"),
    path("recent", views.recentMessage, name="recent_message_message"),
]