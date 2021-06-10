from django.db import models
from core.models import MovieModel

import uuid

# Create your models here.

class MovieSessionModel(models.Model):
    """ Model to store the session IDs. We store them to avoid creating duplicate ID sessions """

    sessionID = models.UUIDField(unique=True, null=False, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name="movie_session")
    sessionStatus = models.JSONField(null=True, blank=True, default=dict)
