from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager


# from apps.movies.models import Movie


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    code = models.IntegerField()
    email = models.EmailField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email}, {self.code}'


class Follow(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_from} is following {self.user_to}'


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='favorite_users')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} liked {self.movie.title}"


class MovieRecommend(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_recommend_to_user')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommended_movies')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='recommended')
    created = models.DateTimeField(auto_now_add=True)


class MovieRecommendAnswer(models.Model):
    ANSWER_STATUS = (
        ('Liked', 'Liked'),
        ('Watched', 'Watched'),
        ('NotLiked', 'NotLiked')
    )
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_recommended')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_got_recommended')
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='answer_recommended')
    answer_status = models.CharField(choices=ANSWER_STATUS, max_length=10)
    created = models.DateTimeField(auto_now_add=True)