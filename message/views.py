from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes

from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.conf import settings

# Import the forms for verification of inputs
from .forms import SessionForm, MessageForm, recentMessageForm

# Import models
from .models import MessageModel
from movie.models import MovieSessionModel

# Import Async fuctions
from asgiref.sync import sync_to_async

# Extra imports
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken

# Set the encryption key for the message
fernet = Fernet(settings.ENCRYPTION_KEY)

# Create your views here.

@sync_to_async
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def fetchAllMessages(request):
    """ Fetch all the messages for that session """

    if request.method == "GET":

        form = SessionForm(request.GET)

        # Check if the form is valid
        if form.is_valid():

            try:

                # Get movie session
                movie_session = MovieSessionModel.objects.get(sessionID=form.cleaned_data.get("sessionID"))

                # Catch error if messages for the session don't exist
                try:
                    # Get the messages for the movie session
                    dataResult = MessageModel.objects.get(sessionID=movie_session)

                    test_list = dataResult.messages
                    test_list.reverse()                    
                    page_obj = Paginator(test_list, 10)

                    # Check if the cursor is present and set the next page else set the next page to 0
                    if form.cleaned_data.get("cursor") and form.cleaned_data.get("cursor") >= 0:
                        next_page = form.cleaned_data.get("cursor")
                    else:
                        next_page = 0

                    # Structure messages
                    result_msg = []
                    for message in page_obj.get_page(next_page):
                        result_msg.append(message)

                    # Decrypt the messages
                    for a in range(len(result_msg)):
                        try:
                            result_msg[a]["message"] = fernet.decrypt(result_msg[a]["message"].encode()).decode()
                        except InvalidToken:
                            result_msg[a]["message"] = result_msg[a]["message"]

                    # Check the cursor of the message list
                    if page_obj.num_pages > 1:
                        cursor = next_page + 1
                    else:
                        cursor = None

                    contentData = {
                        "messages": result_msg,
                        "cursor": cursor,
                    }

                    # Return the messages
                    return JsonResponse({"status": 200, "data": contentData}, status=200)

                except MessageModel.DoesNotExist:

                    initial_msg = {
                            "id": 0,
                            "status": "alert",
                            "username": request.user.username,
                            "user_id": request.user.pk,
                            "message": fernet.encrypt(f"{request.user.username} has started the movie session.".encode()).decode("utf-8"),
                            "date": str(datetime.utcnow()),
                        }

                    # Create the first message in the movie session
                    dataResult = MessageModel.objects.create(
                        sessionID=movie_session,
                        messages=[initial_msg]
                    )

                    dataResult.save() # Save the changes

                    contentData = {
                        "messages": {
                            "id": 0,
                            "status": "alert",
                            "username": request.user.username,
                            "user_id": request.user.pk,
                            "message": f"Started the movie session.",
                            "date": str(datetime.utcnow()),
                        },
                        "cursor": None,
                    }

                    return JsonResponse({"status": 200, "data": contentData}, status=200)
            
            except MovieSessionModel.DoesNotExist:
                return JsonResponse({"status": 404, "message": "Movie session not found!"}, status=404)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)
    else:
        # Warn the user that they are doing a wrong method request
        return JsonResponse({"status": 405, "message": "Method must be GET!"}, status=405)


@sync_to_async
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def newMessage(request):
    """ Receive messages that are sent from the front end """

    if request.method == "POST":

        form = MessageForm(request.data)

        # Check if form is valid
        if form.is_valid():

            try:
                # Get the movie session
                movie_session = MovieSessionModel.objects.get(sessionID=form.cleaned_data.get("sessionID"))

                # Check if the session message has any messages and append the new message
                try:
                    # Get the messages for the movie session
                    dataResult = MessageModel.objects.get(sessionID=movie_session)

                    # Get the list of messages
                    message_list = dataResult.messages
                    
                    # Add message to the list of messages
                    message_list.append({
                        "id": message_list[(len(message_list) - 1) if len(message_list) else 0]["id"] + 1,
                        "status": form.cleaned_data.get("status"),
                        "username": request.user.username,
                        "user_id": request.user.pk,
                        "message": fernet.encrypt(form.cleaned_data.get("message").encode()).decode("utf-8"),
                        "date": str(datetime.utcnow()),
                    })

                    dataResult.save() # Save the changes
                except MessageModel.DoesNotExist:

                    # Create the first message in the movie session
                    dataResult = MessageModel.objects.create(
                        sessionID=movie_session,
                        messages=[{
                            "id": 0,
                            "status": form.cleaned_data.get("status"),
                            "username": request.user.username,
                            "user_id": request.user.pk,
                            "message": fernet.encrypt(form.cleaned_data.get("message").encode()).decode("utf-8"),
                            "date": str(datetime.utcnow()),
                        }]
                    )

                    dataResult.save() # Save the changes

                return JsonResponse({"status": 200, "message": "Message successfully received."}, status=200)
            except MovieSessionModel.DoesNotExist:
                return JsonResponse({"status": 404, "message": "Movie session not found!"}, status=404)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)
    else:
        # Warn the user that they are doing a wrong method request
        return JsonResponse({"status": 405, "message": "Method must be POST!"}, status=405)


@sync_to_async
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def recentMessage(request):
    """ View to check for recent messages """

    if request.method == "GET":

        form = recentMessageForm(request.GET)

        # Check if form is valid
        if form.is_valid():

            try:
                movie_session = MovieSessionModel.objects.get(sessionID=form.cleaned_data.get("sessionID"))

                # Check if the session has a message model
                try:
                    resultData = MessageModel.objects.get(sessionID=movie_session)

                    # Get the messages that are older than the recent the user has
                    result = []
                    for message in resultData.messages:
                        if form.cleaned_data.get("messageID") < message["id"]:
                            result.append(message)

                    # Decrypt the messages
                    for a in range(len(result)):
                        try:
                            result[a]["message"] = fernet.decrypt(result[a]["message"].encode()).decode()
                        except InvalidToken:
                            result[a]["message"] = result[a]["message"]

                    return JsonResponse({"status": 200, "data": result}, status=200)
                except MessageModel.DoesNotExist:
                    return JsonResponse({"status": 404, "message": "Movie session has no messages."}, status=404)
            except MovieSessionModel.DoesNotExist:
                return JsonResponse({"status": 404, "message": "Movie session not found!"}, status=404)
        else:
            # If the form is invalid return a error message of what cause the problem
            for error in form.errors.get_json_data():
                return JsonResponse({"status": 400, "message": form.errors.get_json_data()[error][0]["message"]}, status=400)
    else:
        # Warn the user that they are doing a wrong method request
        return JsonResponse({"status": 405, "message": "Method must be POST!"}, status=405)
