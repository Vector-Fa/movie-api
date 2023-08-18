from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import (MovieCommentSerializer, MovieInputSerializer, MovieCardSerializer,
                          MovieDetailOutputSerializer, MovieOutputSerializer, MovieCommentOutputSerializer,
                          GenresOutputSerializer, PublicGenresOutputSerializer, )
from permissions import IsAdmin
from .services import create_comment, add_movie, FavoriteMovieService, check_favorite_movie
from .models import Movie, Genre
from ..exceptions import BadRequestException
from ..utils import is_serializer_valid, get_or_404
from ..custom_response import SuccessResponse, FailureResponse


class AddMovieApi(APIView):
    """
    Admins can add new movies to site
    -> Int[movie_id]
    """
    permission_classes = [IsAdmin]
    serializer_class = MovieInputSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        is_serializer_valid(ser_data)

        data = ser_data.validated_data
        movie_id: int = add_movie(title=data['title'], description=data['description'], genres=data['genres'],
                                  publish_year=data['publish_year'], type=data['type'], thumbnail=data['thumbnail'],
                                  images=data['images'])
        return SuccessResponse({'movie_id': movie_id})


class AddMovieCommentApi(APIView):
    """
    Users can add comment to movies
    -> New[Comment]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MovieCommentSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        is_serializer_valid(ser_data)
        data = ser_data.validated_data

        comment = create_comment(user=request.user, body=data['body'], movie_id=data['movie_id'],
                                 is_spoiler=data['is_spoiler'])
        new_ser_data = MovieCommentOutputSerializer(instance=comment)
        return SuccessResponse({'comment': new_ser_data.data})


class GetNewestMoviesApi(APIView):
    """
    Get the newest movies which has been added to site
    -> List[Movie]
    """
    serializer_class = MovieCardSerializer

    def get(self, request):
        movies = Movie.objects.order_by('created')[:40]
        ser_data = self.serializer_class(instance=movies, many=True)
        return SuccessResponse({'movies': ser_data.data})


class MovieDetailApi(APIView):
    """
    Get all the information like title, comments, images of a movies
    -> Movie
    """
    serializer_class = MovieDetailOutputSerializer

    def get(self, request, movie_id: int):
        movie = Movie.objects.prefetch_related('images', 'comments').filter(id=movie_id).first()
        if movie:
            ser_data = self.serializer_class(instance=movie)
            return SuccessResponse({'movies': ser_data.data})
        raise BadRequestException('No movies found')


class AddFavoriteMovieApi(APIView):
    """
    Add movies to your favorites list
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request, movie_id: int):
        return FavoriteMovieService(movie_id=movie_id, user=request.user).add()


class RemoveFavoriteMovieApi(APIView):
    """
    Add movies to your favorites list
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def delete(self, request, movie_id: int):
        return FavoriteMovieService(movie_id=movie_id, user=request.user).remove()


class GetFavoriteMoviesApi(APIView):
    """
    Get all the added movies to user favorites
    -> List[Movie]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MovieOutputSerializer

    def get(self, request):
        user_favorites = Movie.objects.filter(favorite_users__user=request.user)
        if user_favorites:
            ser_data = self.serializer_class(instance=user_favorites, many=True)
            return SuccessResponse({'movies': ser_data.data})
        return FailureResponse({'message': 'No favorite movie found'})


class SearchMovieApi(APIView):
    """
    Search for movies
    -> List[Movie]
    """
    serializer_class = MovieCardSerializer

    def get(self, request, query: str):
        movies = Movie.objects.filter(title__icontains=query)[:20]
        if movies:
            ser_data = self.serializer_class(instance=movies, many=True)
            return SuccessResponse({'movies': ser_data.data})
        return FailureResponse({'message': 'No movie found'})


class GetGenresApi(APIView):
    """
    Get all added genres, for adding to movie genres in admin panel
    -> List[Genre]
    """
    permission_classes = [IsAdmin]
    serializer_class = GenresOutputSerializer

    def get(self, request):
        genres = Genre.objects.all()
        ser_data = self.serializer_class(instance=genres, many=True)
        return SuccessResponse({'genres': ser_data.data})


class GetMoviesByGenreApi(APIView):
    """
    Get Movies based on a specific genre
    -> List[Movie]
    """
    serializer_class = MovieCardSerializer

    def get(self, request, genre_slug: str):
        genre = get_or_404(Genre, slug=genre_slug)
        movies = genre.movies.all()
        if movies:
            ser_data = self.serializer_class(instance=movies, many=True)
            return SuccessResponse({'movies': ser_data.data})
        return FailureResponse({'message': 'No movie found'})


class GetPublicGenresApi(APIView):
    """
    Get all genres with their picture and color codes for genre page
    -> List[Genre]
    """
    serializer_class = PublicGenresOutputSerializer

    def get(self, request):
        genres = Genre.objects.all()
        ser_data = self.serializer_class(instance=genres, many=True)
        return SuccessResponse({'genres': ser_data.data})


class IsUserFavoriteApi(APIView):
    """
    Check whether the movie is in user favorites or not
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get(self, request, movie_id: int):
        return check_favorite_movie(movie_id, request.user)
