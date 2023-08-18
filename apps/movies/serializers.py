from typing import List

from rest_framework import serializers

from .models import Movie, MovieImage, MovieComment, Genre


class MovieInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    publish_year = serializers.IntegerField()
    type = serializers.ChoiceField(choices=Movie.MOVIE_TYPES)
    description = serializers.CharField()
    thumbnail = serializers.ImageField(max_length=2000)
    images = serializers.ListField(
        child=serializers.ImageField(max_length=2000, allow_empty_file=False)
    )
    genres = serializers.ListField(
        child=serializers.IntegerField(allow_null=False)
    )


class EditMovieInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'publish_year', 'type', 'description', 'thumbnail')


class MovieImageOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieImage
        fields = ('id', 'image')


class MovieImageSerializerTemp(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField(max_length=2000)


class MovieImageSerializer(serializers.Serializer):
    images = serializers.ListField(child=MovieImageSerializerTemp())


class MovieCardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    publish_year = serializers.IntegerField()
    type = serializers.CharField()
    thumbnail = serializers.ImageField()
    favorites_count = serializers.SerializerMethodField()

    def get_favorites_count(self, obj: Movie) -> int:
        return obj.favorite_users.count()


class MovieCommentOutputSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = MovieComment
        fields = ('user', 'body', 'is_spoiler')

    def get_user(self, obj) -> dict:
        return {'id': obj.user.id, 'username': obj.user.username}


class MovieDetailOutputSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    favorites_count = serializers.SerializerMethodField()
    comments = MovieCommentOutputSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('id', 'title', 'publish_year', 'type', 'description', 'thumbnail', 'favorites_count', 'genres',
                  'images', 'comments')

    def get_genres(self, obj: Movie) -> List[str]:
        return [genre.title for genre in obj.genres.all()]

    def get_images(self, obj) -> List[str]:
        return [image.image.url for image in obj.images.all()]

    def get_favorites_count(self, obj: Movie) -> int:
        return obj.favorite_users.count()


class MovieOutputSerializer(serializers.ModelSerializer):
    favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'publish_year', 'type', 'thumbnail', 'favorites_count')

    def get_favorites_count(self, obj: Movie) -> int:
        return obj.favorite_users.count()


class MovieCommentSerializer(serializers.Serializer):
    body = serializers.CharField(max_length=500)
    movie_id = serializers.IntegerField()
    is_spoiler = serializers.BooleanField()


class GenresOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug')


class PublicGenresOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'title', 'slug', 'image', 'color')


class UserRecommendedMovieOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    thumbnail = serializers.ImageField()


class AnswerRecommendedMovieCardOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
