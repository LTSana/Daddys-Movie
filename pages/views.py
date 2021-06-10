
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Get user
from django.contrib.auth.models import User

# Get custom decorations
from .utils.login_excluded import login_excluded

# Create your views here.

# CUSTOM ERROR HANDLERS
#############################################################
def handler404(request, *args, **argv):
	return render(request, "PublicHome/error/404.html", status=404)

def handler403(request, *args, **argv):
	return render(request, "PublicHome/error/403.html", status=403)

def handler500(request, *args, **argv):
	return render(request, "PublicHome/error/500.html", status=500)

def csrf_failure(request, reason=""):
	return render(request, "PublicHome/error/403.html", status=403)
#############################################################

@login_required
def index(request):
	""" Render and display the home page """
	return render(request, "pages/index.html")


def loginPage(request):
    """ Render and display the login page """
    return render(request, "pages/login.html")


@login_required
def addmoviePage(request):
    """ Render and display the add movie page """
    return render(request, "pages/addmovie.html")


@login_required
def watcherPage(request):
    """ Render and display the watcher page """
    return render(request, "pages/watcher.html")
