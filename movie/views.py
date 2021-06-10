from rest_framework import permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings

from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.paginator import Paginator

import json
import requests
import jwt # For JWT Token

# Import FORM
from .forms import MovieSessionForm, MovieIDForm, MovieChatForm

# Import MODELS
from .models import MovieSessionModel

# Import MODELS from core app
from core.models import MovieModel

# Create your views here.

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def createSession(request):
    """ Create a temporary movie session """

    if request.method == "POST":

        # Start the form validation
        form = MovieIDForm(request.data)

        # Check if the form is valid
        if form.is_valid():

            try:
                # Get the movie we are creating the movie session for
                movieData = MovieModel.objects.get(pk=form.cleaned_data.get("movieID"))

                # Create the session ID
                # We store the a database to store the session IDs to prevent duplication of sessions and for persistance incase of the server shutting down
                sessionData = MovieSessionModel.objects.create(movie=movieData)
                sessionData.save()

                # Check if the session has been created
                if sessionData:
                    return JsonResponse({"status": 200, "message": "Movie session created successfully!", "session": sessionData.sessionID}, status=200)
                else:
                    return JsonResponse({"status": 400, "message": "Failed to start the session! Try again."}, status=400)
            except MovieModel.DoesNotExist:
                return JsonResponse({"status": 404, "message": "Movie not found!"}, status=404)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)
    else:
        # Warn the user that they are doing a wrong method request
        return JsonResponse({"status": 405, "message": "Method must be POST!"}, status=405)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def openSession(request):
    """ Used to retrive data about the session """

    if request.method == "GET":

        # Start the form validation
        form = MovieSessionForm(request.GET)

        # Check if the form is valid
        if form.is_valid():

            try:
                # Get the session data
                sessionData = MovieSessionModel.objects.get(sessionID=form.cleaned_data.get("sessionID"))

                movieData = {
                    "id": sessionData.movie.pk,
                    "title": sessionData.movie.title,
                    "source": sessionData.movie.source,
                    "cover": sessionData.movie.coverPicture.url,
                }
                return JsonResponse({"status": 200, "movie": movieData}, status=200)
            except MovieSessionModel.DoesNotExist:
                return JsonResponse({"status": 404, "message": "Movie session not found!"}, status=404)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)
    else:
        # Warn the user that they are doing a wrong method request
        return JsonResponse({"status": 405, "message": "Method must be GET!"}, status=405)
