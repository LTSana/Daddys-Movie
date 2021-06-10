from django.db import models

# Create your models here.

class MovieModel(models.Model):
	""" Model for the database structure of the movies data we will be storing """

	title = models.CharField(
		max_length=1200,
		null=False,
		help_text="This is the field for the name of the movie",
	)

	source = models.URLField(
		null=False,
		help_text="This is the field for the location of the movie. Must be a URL",
	)

	coverPicture = models.ImageField(
		null=False,
		upload_to="cover/",
		help_text="This is the field for the cover image of the movie."
	)
