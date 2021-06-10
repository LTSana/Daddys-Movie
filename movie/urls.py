from django.urls import path

from . import views

urlpatterns = [
	path("create", views.createSession, name="movie_create_session"),
	path("session", views.openSession, name="movie_open_session"),
]