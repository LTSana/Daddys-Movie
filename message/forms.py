from django import forms
from django.utils.html import strip_tags

class SessionForm(forms.Form):
    """ Used to check the session ID """

    sessionID = forms.UUIDField(
        required=True,
        help_text="Session ID is UUID and is required to identify and join a Session.",
        error_messages={
            "required": "Movie Session ID is required! Please provide one.",
            "invalid": "Movie Session ID is invalid! Please provide a UUID.",
        }
    )

    cursor = forms.IntegerField(
        required=False,
        help_text="Cursor to paginate through the messages.",
        error_messages={
            "required": "Cursor is required!",
            "invalid": "Cursor is invalid! Please provide a integer for the cursor."
        }
    )


class MessageForm(forms.Form):
    """ Used to check the messages received by the user """

    sessionID = forms.UUIDField(
        required=True,
        help_text="Session ID is UUID and is required to identify and join a Session.",
        error_messages={
            "required": "Movie Session ID is required! Please provide one.",
            "invalid": "Movie Session ID is invalid! Please provide a UUID.",
        }
    )

    status = forms.CharField(
        required=True,
        help_text="The message status is the type of message (Alert or Message)",
        max_length=2000,
        min_length=1,
        label="Message",
        error_messages={
            "required": "Message status is required! Please provide a message status.",
            "invalid": "Message status is invalid! Please check your message for unwanted characters status.",
            "max_length": "Message status is too long! Please make your message shorter status.",
            "min_length": "Message status is too short! Please make your message a little longer status.",
        }
    )

    message = forms.CharField(
        required=True,
        help_text="The message the user is sending",
        max_length=2000,
        min_length=1,
        label="Message",
        error_messages={
            "required": "Message is required! Please provide a message.",
            "invalid": "Message is invalid! Please check your message for unwanted characters.",
            "max_length": "Message is too long! Please make your message shorter.",
            "min_length": "Message is too short! Please make your message a little longer.",
        }
    )

    def clean(self):
        cleaned_data = super(MessageForm, self).clean()

        # Used to remove html tags from strings
        for item in self.fields.keys():
            try:
                if isinstance(cleaned_data[item], str):
                    cleaned_data[item] = strip_tags(cleaned_data[item])
            except KeyError:
                pass

        return cleaned_data


class recentMessageForm(forms.Form):
    """ Used to check the inputs for looking for the most recent messages """

    sessionID = forms.UUIDField(
        required=True,
        help_text="Session ID is UUID and is required to identify and join a Session.",
        error_messages={
            "required": "Movie Session ID is required! Please provide one.",
            "invalid": "Movie Session ID is invalid! Please provide a UUID.",
        }
    )

    messageID = forms.IntegerField(
        required=True,
        help_text="Most recent message ID from the user.",
        error_messages={
            "required": "Message ID is required! Please provide the message ID of the most recent message",
            "invalid": "Message ID is invalid! Please provide a integer ID."
        }
    )
