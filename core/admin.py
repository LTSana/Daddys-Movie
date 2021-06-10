from django.contrib import admin

# Get the model
from .models import MovieModel

# Register your models here.

admin.site.register(MovieModel)