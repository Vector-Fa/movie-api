from typing import Dict, List

from rest_framework import serializers, status

from .models import User, Follow, MovieRecommendAnswer, MovieRecommend
from ..custom_response import FailureResponse
from apps.movies.serializers import (MovieCardSerializer, UserRecommendedMovieOutSerializer,
                                     AnswerRecommendedMovieCardOutSerializer)
from apps.movies.models import Movie


class EmailRegisterationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserRegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    verify_code = serializers.IntegerField(write_only=True)
    username = serializers.CharField(min_length=3, max_length=60)
    email = serializers.EmailField(max_length=150)
    bio = serializers.CharField(max_length=300, required=False, read_only=True)
    password = serializers.CharField(min_length=6, max_length=40, write_only=True)

    def validate_email(self, value):
        email = User.objects.filter(email=value).exists()
        if email:
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_username(self, value):
        username = User.objects.filter(username=value).exists()
        if username:
            raise serializers.ValidationError("Username already exists")
        return value


class UploadProfileImageSerializer(serializers.Serializer):
    image = serializers.ImageField(required=True, write_only=True)


# TODO: if its for searching for users use another one to not show email
class UserSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    favorite_movies = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "is_admin",
            "photo",
            "follower_count",
            "following_count",
            "favorite_movies"
        )
        read_only_fields = ("id",)

    def get_follower_count(self, obj) -> int:
        return obj.followers.count()

    def get_following_count(self, obj) -> int:
        return obj.followings.count()

    def get_favorite_movies(self, obj) -> List[dict]:
        favorites = Movie.objects.filter(favorite_users__user=obj)
        serializer = MovieCardSerializer(instance=favorites, many=True)
        return serializer.data


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'bio')


class SearchUserOutputSerializer(serializers.Serializer):
    username = serializers.CharField()
    photo = serializers.ImageField()


class UserFollowSerializer(serializers.Serializer):
    user_to = serializers.IntegerField()


class UserFriendListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "photo")


class RecommendMovieToUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    movie_id = serializers.IntegerField()


class AnswerRecommendedMovieSerializer(serializers.Serializer):
    recommend_id = serializers.IntegerField()
    answer_status = serializers.ChoiceField(choices=MovieRecommendAnswer.ANSWER_STATUS)


class GetRecommendedMoviesOutSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user_from.username')
    movie = UserRecommendedMovieOutSerializer()

    class Meta:
        model = MovieRecommend
        fields = ('id', 'username', 'movie')


class AnswerRecommendedMovieOutSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source='user_from.username')
    movie = AnswerRecommendedMovieCardOutSerializer()

    class Meta:
        model = MovieRecommendAnswer
        fields = ('id', 'username', 'movie', 'answer_status')
