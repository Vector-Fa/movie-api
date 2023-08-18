from django.contrib import admin

from .models import Movie, MovieComment, MovieImage, Genre

admin.site.register([Movie, MovieComment, MovieImage, Genre])
