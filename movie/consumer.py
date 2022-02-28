import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
from django.core.paginator import Paginator

# JWT
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTTokenUserAuthentication

# Import models
from django.contrib.auth.models import User

# Import time packages
import jwt
from urllib import parse
from datetime import datetime

# Import forms
from .forms import MovieChatForm, MovieSessionForm, MovieIDForm

class ChatConsumer(WebsocketConsumer):

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))

        return result

    def message_to_json(self, message):

        try:
            user = User.objects.get(pk=message["content"]["pk"])
        except User.DoesNotExist:
            user = {"username": "User does not exist anymore!"}

        return {
            "status": message["content"]["status"],
            "username": user.username,
            "content": message["content"]["message"],
            "timestamp": str(message["content"]["timestamp"]),
        }

    def new_message(self, data):

        # Check if the scope user session is being used
        try:
            # Get the user from the scope
            user = User.objects.get(username=self.scope["user"])

            # Check if the user exists and get their ID (Primary Key)
            if user:
                user_id = user.pk
        except User.DoesNotExist:

            if parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0] and settings.DEBUG:
                # Validate the token and check who it belongs to also check if anything is wrong with the token
                valid_data = None # Initialize variable
                user_id = None # Initialize variable
                try:
                    valid_data = jwt.decode(parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0], settings.SECRET_KEY, algorithms=api_settings.ALGORITHM)
                except jwt.ExpiredSignatureError:
                    print("Token Expired, Please Login")
                except jwt.DecodeError:
                    print("Token Modified by thirdparty")
                except jwt.InvalidTokenError:
                    print("Invalid Token")
                except Exception as e:
                    print(e)

                # Check if the token belongs to any users
                try:
                    if valid_data:
                        user_id = valid_data['user_id']
                    else:
                        print("User not found!")
                except KeyError:
                    print("User not found!")
            else:
                # Set user ID to none
                user_id = None

            # Check if the token belongs to any users
            try:
                if valid_data:
                    user_id = valid_data['user_id']
                else:
                    print("User not found!")
            except KeyError:
                print("User not found!")

        form = MovieChatForm(data)

        # Check if the user ID is available (Meaning the user is logged in)
        if user_id:

            # Check if the form is valid
            if form.is_valid():

                # Check if the user is in our system
                try:
                    user = User.objects.get(pk=user_id)

                    # Create the dict of the message for storage in the database
                    message = {
                        "content": {
                            "status": "message",
                            "pk": user.pk,
                            "message": form.cleaned_data.get("message"),
                            "timestamp": str(datetime.utcnow()), # Must save in string form
                        },
                    }

                    # Send the content to message_to_json
                    content = {
                        "command": "new_message",
                        "message": self.message_to_json(message),
                    }
                except User.DoesNotExist:
                    message = {
                        "content": {
                            "status": "aler_message",
                            "pk": user_id,
                            "message": "You need to login!",
                            "timestamp": str(datetime.utcnow()), # Must save in string form
                        },
                    }

                    # Send the content to message_to_json
                    content = {
                        "command": "new_message",
                        "message": self.message_to_json(message),
                    }

                return self.send_chat_message(content)

            else:
                # If the form is invalid return a error message of what cause the problem
                for error in form.errors.get_json_data():
                    message = {        
                        "content": {
                            "status": "aler_message",
                            "pk": user_id,
                            "message": form.errors.get_json_data()[error][0]["message"],
                            "timestamp": str(datetime.utcnow()), # Must save in string form
                        },
                    }

                    # Send the content to message_to_json
                    content = {
                        "command": "new_message",
                        "message": self.message_to_json(message),
                    }

                    return self.send_chat_message(content)
        else:
            message = {
                "content": {
                    "status": "aler_message",
                    "pk": user_id,
                    "message": "User ID is required!",
                    "timestamp": str(datetime.utcnow()), # Must save in string form
                },
            }

            # Send the content to message_to_json
            content = {
                "command": "new_message",
                "message": self.message_to_json(message),
            }

            return self.send_chat_message(content)

    def videoControl(self, data):

        # Initialize
        movieControlData = {}
        
        # Check if the scope user session is being used
        try:
            # Get the user from the scope
            user = User.objects.get(username=self.scope["user"])

            # Check if the user exists and get their ID (Primary Key)
            if user:
                user_id = user.pk
        except User.DoesNotExist:

            if parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0] and settings.DEBUG:
                # Validate the token and check who it belongs to also check if anything is wrong with the token
                valid_data = None # Initialize variable
                user_id = None # Initialize variable
                try:
                    valid_data = jwt.decode(parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0], settings.SECRET_KEY, algorithms=api_settings.ALGORITHM)
                except jwt.ExpiredSignatureError:
                    print("Token Expired, Please Login")
                except jwt.DecodeError:
                    print("Token Modified by thirdparty")
                except jwt.InvalidTokenError:
                    print("Invalid Token")
                except Exception as e:
                    print(e)

                # Check if the token belongs to any users
                try:
                    if valid_data:
                        user_id = valid_data['user_id']
                    else:
                        print("User not found!")
                except KeyError:
                    print("User not found!")
            else:
                # Set user ID to none
                user_id = None

            # Check if the token belongs to any users
            try:
                if valid_data:
                    user_id = valid_data['user_id']
                else:
                    print("User not found!")
            except KeyError:
                print("User not found!")

        if user_id:

            try:
                userData = User.objects.get(pk=user_id)

                if data:
                    try:
                        movieControlData = {
                            "action": data["action"],
                            "username": userData.username,
                            "currentTime": data["currentTime"],
                        }
                    except ValueError:
                        movieControlData = {
                            "action": "",
                            "username": "",
                            "currentTime": "",
                        } 
                else:
                    movieControlData = {
                        "action": "",
                        "username": "",
                        "currentTime": "",
                    }
            except User.DoesNotExist:
                movieControlData = {
                    "action": "",
                    "username": "",
                    "currentTime": "",
                }    
        else:
            movieControlData = {
                "action": "",
                "username": "",
                "currentTime": "",
            }
        return self.send_chat_message(movieControlData)

    commands = {
        "new_message": new_message,
        "video_controls": videoControl,
    }

    async def connect(self):
        # Used for Authentication

        #print(jwt.decode(parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0], settings.SECRET_KEY, algorithms=api_settings.ALGORITHM))

        # Validate the room UUID
        form =  MovieSessionForm({"sessionID": self.scope['url_route']['kwargs']['sessionID']})

        print(f"FORM: {form.is_valid()}")
        print("LOL")
        
        # Check if the form is valid
        if form.is_valid():

            self.room_name = self.scope['url_route']['kwargs']['sessionID']
            self.room_group_name = 'chat_%s' % self.room_name

            print(f"BEFORE")

            print(self.scope["user"])
            print(self.scope['url_route']['kwargs']['sessionID'])
            print('chat_%s' % self.room_name)
            print(self.channel_name)

            print("POINT 1")
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            print(f"AFTER")

            # Check if the scope user session is being used
            try:
                # Get the user from the scope
                user = User.objects.get(username=self.scope["user"])

                # Check if the user exists and get their ID (Primary Key)
                if user:
                    user_id = user.pk
            except User.DoesNotExist:

                if parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0] and settings.DEBUG:
                    # Validate the token and check who it belongs to also check if anything is wrong with the token
                    valid_data = None # Initialize variable
                    user_id = None # Initialize variable
                    try:
                        valid_data = jwt.decode(parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0], settings.SECRET_KEY, algorithms=api_settings.ALGORITHM)
                    except jwt.ExpiredSignatureError:
                        print("Token Expired, Please Login")
                    except jwt.DecodeError:
                        print("Token Modified by thirdparty")
                    except jwt.InvalidTokenError:
                        print("Invalid Token")
                    except Exception as e:
                        print(e)

                    # Check if the token belongs to any users
                    try:
                        if valid_data:
                            user_id = valid_data['user_id']
                        else:
                            print("User not found!")
                    except KeyError:
                        print("User not found!")
                else:
                    # Set user ID to none
                    user_id = None

            # Check if the user is logged in and accept connection else deny
            if user_id:
                self.accept()
            else:
                self.disconnect("Disconnecting")

    def disconnect(self, close_code):
        # Leave room group
        print("LOL DISCONNECTED!")
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)

        print("?")
        print(data)
        
        #message = data['message']
        if data["command"]:
            self.commands[data["command"]](self, data)


    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, data):
        # Send message to WebSocket
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


class MovieStatusConsumer(WebsocketConsumer):
    """ Used to check all users in sync during the movie session """

    def videoControl(self, data):
        return self.send_message({"action": "pause"})

    commands = {
        "video_controls": videoControl,
    }

    def connect(self):
        # Used for Authentication

        #print(jwt.decode(parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0], settings.SECRET_KEY, algorithms=api_settings.ALGORITHM))

        # Validate the room UUID
        form =  MovieSessionForm({"sessionID": self.scope['url_route']['kwargs']['sessionID']})

        # Check if the form is valid
        if form.is_valid():

            self.room_name = self.scope['url_route']['kwargs']['sessionID']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            # Check if the scope user session is being used
            try:
                # Get the user from the scope
                user = User.objects.get(username=self.scope["user"])

                # Check if the user exists and get their ID (Primary Key)
                if user:
                    user_id = user.pk
            except User.DoesNotExist:

                if parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0] and settings.DEBUG:
                    # Validate the token and check who it belongs to also check if anything is wrong with the token
                    valid_data = None # Initialize variable
                    user_id = None # Initialize variable
                    try:
                        valid_data = jwt.decode(parse.parse_qs(self.scope["query_string"].decode("UTF-8"))["token"][0], settings.SECRET_KEY, algorithms=api_settings.ALGORITHM)
                    except jwt.ExpiredSignatureError:
                        print("Token Expired, Please Login")
                    except jwt.DecodeError:
                        print("Token Modified by thirdparty")
                    except jwt.InvalidTokenError:
                        print("Invalid Token")
                    except Exception as e:
                        print(e)

                    # Check if the token belongs to any users
                    try:
                        if valid_data:
                            user_id = valid_data['user_id']
                        else:
                            print("User not found!")
                    except KeyError:
                        print("User not found!")
                else:
                    # Set user ID to none
                    user_id = None

            # Check if the user is logged in and accept connection else deny
            if user_id:
                self.accept()
            else:
                self.disconnect("Disconnecting")

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        #message = data['message']
        if data["command"]:
            self.commands[data["command"]](self, data)


    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, data):
        # Send movie actions to WebSocket
        self.send(text_data=json.dumps(data))
