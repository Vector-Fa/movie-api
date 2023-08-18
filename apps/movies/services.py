from typing import Union, List

from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from .models import Movie, MovieComment, MovieImage
from apps.users.models import FavoriteMovie
from apps.users.models import User
from .utils import get_genre_objects
from ..utils import get_or_404
from ..exceptions import BadRequestException, SomethingWentWrongException
from ..custom_response import SuccessResponse, FailureResponse


def add_movie(thumbnail, images, genres: List[int], **kwargs) -> int:
    genres = get_genre_objects(genres)
    with transaction.atomic():
        try:
            movie = Movie(**kwargs, thumbnail=thumbnail)
            movie.save()
            movie.genres.set(genres)

            for image in images:
                MovieImage.objects.create(movie=movie, image=image)

            return movie.id
        except Exception:
            raise SomethingWentWrongException('Movie could not be added, try again')


def create_comment(body: str, movie_id: int, user: User, is_spoiler: bool) -> MovieComment:
    movie = get_or_404(Movie, id=movie_id)
    comment = MovieComment.objects.create(user=user, movie=movie, body=body, is_spoiler=is_spoiler)
    return comment


class FavoriteMovieService:
    def __init__(self, movie_id: int, user: User):
        self.user = user
        self.movie_id = movie_id

    def add(self):
        movie = get_or_404(Movie, id=self.movie_id)
        favorite_movie = self._get_favorite_movie_query()
        if favorite_movie.exists():
            raise BadRequestException('movies is already added to your list')

        FavoriteMovie.objects.create(
            movie=movie, user=self.user
        )
        return SuccessResponse({'message': 'Added to your favorite movies'})

    def remove(self):
        favorite_movie = self._get_favorite_movie_query()
        if not favorite_movie.exists():
            raise BadRequestException('movies is not in your list')
        favorite_movie.delete()
        return SuccessResponse({'message': 'Removed from your favorite movies'})

    def _get_favorite_movie_query(self):
        return FavoriteMovie.objects.filter(movie=self.movie_id, user=self.user)


def check_favorite_movie(movie_id: int, user: User):
    if FavoriteMovie.objects.filter(movie__pk=movie_id, user=user).exists():
        return SuccessResponse({'message': 'exists'})
    return FailureResponse({'message': 'not exists'})
