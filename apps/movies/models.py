from django.db import models

from apps.users.models import User


class Movie(models.Model):
    MOVIE_TYPES = (
        ('Serial', "Serial"),
        ('Movie', 'Movie'),
        ('Game', 'Game'),
    )
    title = models.CharField(max_length=50)
    publish_year = models.IntegerField()
    type = models.CharField(choices=MOVIE_TYPES, max_length=10)
    description = models.TextField()
    thumbnail = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField('Genre', related_name='movies')

    def __str__(self):
        return self.title


class Genre(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    image = models.ImageField()
    color = models.CharField(max_length=7)

    def __str__(self):
        return f"{self.title}"


class MovieImage(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField()

    def __str__(self):
        return f"{self.movie.title} - {self.image.name}"


class MovieComment(models.Model):
    body = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    is_spoiler = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:30]

