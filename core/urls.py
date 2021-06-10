from django.urls import path

from . import views

urlpatterns = [
	path("currentUser", views.currentUser, name="core_currentUser"),
	path("login", views.loginAPI, name="core_login"),
	path("logout", views.logoutAPI, name="core_logout"),
	path("movies", views.movies, name="core_movies"),
]