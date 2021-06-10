from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="pages_home"),
    path("index", views.index, name="pages_home"),
    path("login", views.loginPage, name="pages_login"),
    path("addmovie", views.addmoviePage, name="pages_addmovie"),
    path("watcher", views.watcherPage, name="pages_watcher"),
]