from rest_framework import permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings

from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages

from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate
from django.db.models import Q
from django.core.paginator import Paginator

import json
import requests
import jwt # For JWT Token

# Used for Images
import io
import base64
import secrets
from PIL import Image
from django.core.files.base import ContentFile

# IMPORT CUSTOM FORMS
from .forms import LoginForm, MovieForm

# IMPORT MODELS
from .models import MovieModel

# Create your views here.

@api_view(['GET'])
def currentUser(request):
    """ Show the current user """

    if request.user.is_authenticated:
        return JsonResponse({'status': 200, 'message': 'You are logged in!', 'data': {'username': request.user.username, "userID": request.user.pk}}, status=200)
    else:
        return JsonResponse({'status': 404, 'message': 'You are not logged in.'}, status=404)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def loginAPI(request):
    """ Authenticate the user into the a session """

    if request.method == "POST":

        # Get the form and pass the data
        form = LoginForm(request.data)

        # Check if the form is valid
        if form.is_valid():

            # Check if reCAPTCHA is valid
            secret_key = settings.RECAPTCHA_SECRET_KEY # Get the key from django settings

            # captcha verification
            try:
                # captcha verification
                data = {
                    'response': request.data.get('recaptcha_token'),
                    'secret': secret_key
                }
            except KeyError:
                return JsonResponse({"status": 400, "message": "reCAPTCHA token missing."}, status=400)

            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result_json = resp.json()

            # Check if reCAPTCHA passed
            if result_json.get("success"):

                # Authenticate the user
                user = authenticate(
                    request,
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password"),
                )

                # Check if any user was returned
                if user is not None:

                    # Login the user
                    login(request, user)

                    # Generate and return the users JWT token for later authentication
                    # TOKEN GENERATION WILL BE DISABLED BECAUSE WE ARE RUNNING OFF THE BACK-END ALREADY
                    # TOKENS ARE NOT REQUIRED. WE ARE USING SESSIONS
                    token = {}
                    if settings.DEBUG: # ONLY USE JWT(Authentication Tokens) when debugging
                        payload = RefreshToken.for_user(user)

                        token["access"] = str(payload.access_token)
                        token["refresh"] = str(payload)
                        token["type"] = "Bearer"
                        token["expire"] = api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()

                    return JsonResponse({"status": 200, "user":{"username": user.username, "id": user.pk}, "token": token}, status=200)
                else:
                    # Tell the user that the password or username is wrong
                    return JsonResponse({"status": 401, "message": "Login failed! Username or password is wrong."}, status=401)
            else:
                # Tell the user that the reCAPTCHA failed
                return JsonResponse({"status": 401, "message": "Failed reCAPTCHA! Try again.", "alert": "warning"}, status=401)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)
    else:
        # Warn the user that they are doing a wrong method request
        return JsonResponse({"status": 405, "message": "Method must be POST!"}, status=405)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def logoutAPI(request):
    """ Logout the user """

    if request.user.is_authenticated:

        # Logout the user
        logout(request)

        return JsonResponse({"status": 200, "message": "You've logged out successfully!"}, status=200)
    else:
        return JsonResponse({"status": 404, "message": "You need to be logged in to logout!"}, status=404)


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticated])
def movies(request):
    """ Used to get the movies and also remove movies or add them """

    # Check what request method we are receiving
    if request.method == "GET":

        # Get the form and pass the data
        form = MovieForm(request.GET)

        # Check if the form is valid
        if form.is_valid():

            # Fetch the movies
            if form.cleaned_data.get("action") == "fetch":

                try:
                    if form.cleaned_data.get("movieID"):
                        # Get the movies by ID(Primary Key)
                        movie = MovieModel.objects.get(pk=form.cleaned_data.get("movieID"))

                        movieJSON = {
                            "id": movie.pk,
                            "title": movie.title,
                            "source": movie.source,
                            "cover": str(movie.coverPicture.url),
                        }
                        return JsonResponse({"status": 200, "movie": movieJSON}, status=200)

                    elif form.cleaned_data.get("title"):
                        # Get the movies by title
                        movies = MovieModel.objects.filter(title__contains=form.cleaned_data.get("title"))
                    else:
                        # Get all the movies
                        movies = MovieModel.objects.all()

                    # Make a list of all the movies to send through JSON
                    movie_list = []
                    for movie in movies:
                        movie_list.append({
                            "id": movie.pk,
                            "title": movie.title,
                            "source": movie.source,
                            "cover": str(movie.coverPicture.url),
                        })

                    return JsonResponse({"status": 200, "movies": movie_list}, status=200)
                except MovieModel.DoesNotExist:
                    return JsonResponse({"status": 404, "message": "Movie not found!"}, status=404)
            else:
                return JsonResponse({"status": 400, "message": "Please provide a action option. Action recommended for this request: Fetch"}, status=400)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)

    elif request.method == "POST":

        # Get the form and pass the data
        form = MovieForm(request.data)

        # Check if the form is valid
        if form.is_valid():

            # Add movies
            if form.cleaned_data.get("action") == "add":

                # Get the image from the request
                body = request.data

                # Prevent a KeyError incase the json doesn't have 'coverPicture'
                try:
                    coverPicture = body['coverPicture']
                except KeyError:
                    return JsonResponse({"status": 400, "message": "Cover Picture is required! Please upload a coverPicture"}, status=400)

                # getting the file format and the necessary dataURl for the file
                _format, _dataurl = coverPicture.split(';base64,')

                # file name and extension
                _filename, _extension = secrets.token_hex(20), _format.split('/')[-1]

                if _extension.lower() in ["jpeg", "jpg", "png"]:

                    # getting the file format and the necessary dataURl for the file
                    _format, _dataurl = coverPicture.split(';base64,')
                    # file name and extension
                    _filename, _extension = secrets.token_hex(20), _format.split('/')[-1]

                    # generating the contents of the file
                    file = ContentFile(base64.b64decode(_dataurl), name=f"{_filename}.{_extension}")

                    # opening the file with the pillow
                    image = Image.open(file)
                    # using BytesIO to rewrite the new content without using the filesystem
                    image_io = io.BytesIO()

                    # Resize
                    base_width=600

                    # resize
                    w_percent = (base_width/float(image.size[0]))
                    h_size = int((float(image.size[1])*float(w_percent)))
                    image = image.resize((base_width,h_size), Image.ANTIALIAS)

                    # save resized image
                    image.save(image_io, format=_extension)

                    # Check the image size and make sure it's not greater than 9 megabytes
                    if int(image_io.tell() / 1024) <= 900:
                        # generating the content of the new image
                        file = ContentFile(image_io.getvalue(), name=f"{_filename}.{_extension}" )

                        # Check if the movie link is from Dropbox
                        movie_link = form.cleaned_data.get("link")
                        if "dropbox.com" in movie_link:
                            movie_link = str(movie_link).replace("?dl=0", "?raw=1")

                        movieData = MovieModel.objects.create(
                            title=form.cleaned_data.get("title"),
                            source=movie_link,
                            coverPicture=file,
                        )
                        movieData.save()

                        movie_data = {
                            "id": movieData.pk,
                            "title": movieData.title,
                            "source": movieData.source,
                            "cover": str(movieData.coverPicture.url),
                        }

                        return JsonResponse({"status": 200, "message": "Successfully added the movie!", "data": movie_data}, status=200)
                    else:
                        return JsonResponse({"status": 401, "message": "Cover picture is too big! Cover picture must be less than 9Mbs(megabytes)."}, status=401)
                else:
                    return JsonResponse({"status": 401, "message": "Picture is the wrong format! Please only upload PNG, JPEG or JPG."}, status=401)

            # Delete movies
            elif form.cleaned_data.get("action") == "delete":

                try:
                    # Remove the movie from the database
                    movie_data = MovieModel.objects.get(pk=form.cleaned_data.get("movieID"))
                    movie_data.delete()
                    return JsonResponse({"status": 200, "message": "Movie was successfully deleted!"}, status=200)
                except MovieModel.DoesNotExist:
                    return JsonResponse({"status": 404, "message": "Movie not found!"}, status=404)
            else:
                return JsonResponse({"status": 400, "message": "Please provide a action option. Action recommended for this request: Add or Delete"}, status=400)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)
    else:
        # Warn the user that they are doing a wrong method request
        return JsonResponse({"status": 405, "message": "Method must be POST or GET!"}, status=405)
