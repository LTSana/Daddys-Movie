from django.db import models
from movie.models import MovieSessionModel

# Create your models here.

class MessageModel(models.Model):
    """ For keeping track of messages of the movie session """

    sessionID = models.ForeignKey(MovieSessionModel, on_delete=models.CASCADE, related_name="messages")
    messages = models.JSONField(default=list, help_text="All the chats for the movie session", blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sessionID} | {self.date}"
