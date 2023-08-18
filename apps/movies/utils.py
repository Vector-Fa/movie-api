from typing import List

from .models import Genre
from ..exceptions import BadRequestException


def get_genre_objects(genres_id: List[int]) -> List[Genre]:
    genres = []
    for genre_id in genres_id:
        try:
            genres.append(Genre.objects.get(id=genre_id))
        except Genre.DoesNotExist:
            raise BadRequestException(f'Genre with id ({genre_id}) does not exists')
    return genres
