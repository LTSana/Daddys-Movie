from django import forms
from django.utils.html import strip_tags

class MovieIDForm(forms.Form):
    """ Used to validate the movie ID """

    movieID = forms.IntegerField(
        min_value=0,
        required=True,
        label="Movie ID",
        help_text="The movie ID to look for the movie",
        error_messages={
            "invalid": "Movie ID is invalid! Please make sure it is an integer.",
            "min_value": "Movie ID is invalid! Please make sure it is a positive integer",
            "required": "Movie ID is required! Please provide one",
        }
    )


class MovieSessionForm(forms.Form):
    """ Used to validate the for UUID """

    sessionID = forms.UUIDField(
        required=True,
        help_text="Session ID is UUID and is required to identify and join a Session.",
        error_messages={
            "required": "Movie Session ID is required! Please provide one.",
            "invalid": "Movie Session ID is invalid! Please provide a UUID.",
        }
    )


class MovieChatForm(forms.Form):
    """ Used to validate the movie chat """

    sessionID = forms.UUIDField(
        required=True,
        help_text="Session ID is UUID and is required to identify and join a Session.",
        error_messages={
            "required": "Movie Session ID is required! Please provide one.",
            "invalid": "Movie Session ID is invalid! Please provide a UUID.",
        }
    )

    message = forms.CharField(
        required=True,
        help_text="The message the user is sending to the chat room",
        label="message",
        max_length=2000,
        min_length=1,
        error_messages={
            "required": "Message is required! Please enter a message to send.",
            "min_length": "Message is too short!",
            "max_length": "Message is too long! Please shorten your message",
            "invalid": "Message is invalid! Please make sure your message does not contain any unwanted symbols.",
        }
    )

    def clean(self):
        cleaned_data = super(MovieChatForm, self).clean()

        # Used to remove html tags from strings
        for item in self.fields.keys():
            try:
                if isinstance(cleaned_data[item], str):
                    cleaned_data[item] = strip_tags(cleaned_data[item])
            except KeyError:
                pass

        return cleaned_data
