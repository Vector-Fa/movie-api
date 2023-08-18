import random
from datetime import timedelta

from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from .models import User, Follow, VerifyCode, MovieRecommend, MovieRecommendAnswer
from apps.movies.models import Movie
from ..utils import get_or_404
from .tasks import send_email_task, upload_profile_image_task
from ..exceptions import BadRequestException, NotFoundException, ForbiddenException
from ..custom_response import SuccessResponse, FailureResponse


def check_registration_email(email: str):
    if User.objects.filter(email=email).exists():
        raise BadRequestException('email already exists')

    two_minute_ago = timezone.now() - timedelta(minutes=2)
    if VerifyCode.objects.filter(email=email, created__gte=two_minute_ago).exists():
        raise BadRequestException('Code is already sent wait 2 minutes')

    verify_code = random.randint(1000, 99999)
    VerifyCode.objects.update_or_create(
        email=email, defaults={'code': verify_code}
    )

    send_email_task(email=email, verify_code=verify_code).delay()
    return SuccessResponse({'message': 'code sent'})


def register_user(verify_code: int, **kwargs) -> User:
    two_minute_ago = timezone.now() - timedelta(minutes=2)
    verify_code_object = VerifyCode.objects.filter(
        code=verify_code, created__gte=two_minute_ago, email=kwargs['email']
    ).first()
    if not verify_code_object:
        raise BadRequestException('Code is invalid or expired')

    verify_code_object.delete()
    return User.objects.create_user(**kwargs)


class UploadProfileImageService:
    CONSTANT_PATH = 'media/profiles/'

    def upload(self, image, user: User):
        image_path = f'{self.CONSTANT_PATH}/{user.username}.png'
        storage = FileSystemStorage()
        if not storage.exists(image_path):
            storage.save(image_path, File(image))
            upload_profile_image_task(image_path=storage.path(image_path), user_id=user.id).delay()
            return SuccessResponse({'message': 'photo is uploading'}, status=status.HTTP_200_OK)
        raise ForbiddenException('wait to upload your last image first')


class UserFollowService:
    def __init__(self, user: User, to_username: str):
        self.user = user
        self.to_username = to_username

    def follow(self) -> Response:
        self._is_self()
        user_to = self._get_user_to()

        if Follow.objects.filter(user_from=self.user, user_to=user_to).exists():
            raise BadRequestException('You are already following this user')
        Follow.objects.create(user_from=self.user, user_to=user_to)
        return SuccessResponse({'message': 'followed successfully'})

    def unfollow(self):
        self._is_self()
        user_to = self._get_user_to()

        if not Follow.objects.filter(user_from=self.user, user_to=user_to).exists():
            raise BadRequestException('You are not following this user')
        Follow.objects.get(user_from=self.user, user_to=user_to).delete()
        return SuccessResponse({'message': 'unfollowed successfully'})

    def _is_self(self) -> None:
        if self.user.username == self.to_username:
            raise BadRequestException('you cant do this operation on your self')

    def _get_user_to(self) -> User:
        user_to = User.objects.filter(username=self.to_username).first()
        if user_to:
            return user_to
        raise NotFoundException('user does not exists')


class FollowListService:
    @staticmethod
    def get_followers(user: User):
        return User.objects.filter(followings__user_to=user)

    @staticmethod
    def get_followings(user: User):
        return User.objects.filter(followers__user_from=user)


def search_user(query: str):
    users = User.objects.filter(Q(username__icontains=query))[:30]
    if users:
        return users
    return None


def is_user_friend(username: str, user: User):
    if Follow.objects.filter(user_from=user, user_to__username=username).exists():
        return SuccessResponse({'message': 'exists'})
    return FailureResponse({'message': 'doesn\'t exists'})


class MovieRecommendService:
    def __init__(self, user_from: User):
        self.user_from = user_from

    def recommend_to_user(self, username_to: str, movie_id: int):
        user_to = self._get_user_to(username_to)
        self._does_movie_exists(movie_id)

        if not Follow.objects.filter(user_from=self.user_from, user_to=user_to).exists():
            raise ForbiddenException('You are not following this user')

        if MovieRecommend.objects.filter(user_from=self.user_from, user_to=user_to, movie_id=movie_id).exists():
            raise BadRequestException('You already sent this movie recommendation to user')

        MovieRecommend.objects.create(user_from=self.user_from, user_to=user_to, movie_id=movie_id)
        return SuccessResponse({'message': 'recommendation sent'})

    def answer_recommended_movie(self, answer_status: str, recommend_id: int):
        recommended_movie: MovieRecommend = MovieRecommend.objects.filter(pk=recommend_id).first()
        if not recommended_movie:
            raise BadRequestException('This recommendation does not exists')

        MovieRecommendAnswer.objects.create(user_from=self.user_from, user_to=recommended_movie.user_from,
                                            movie_id=recommended_movie.movie_id, answer_status=answer_status)
        recommended_movie.delete()
        return SuccessResponse({'message': 'recommendation sent'})

    def _get_user_to(self, username_to: str) -> User:
        if self.user_from.username == username_to:
            raise ForbiddenException('Cant do this operation on yourself')
        return get_or_404(User, username=username_to)

    def _does_movie_exists(self, movie_id) -> None:
        if not Movie.objects.filter(pk=movie_id).exists():
            raise BadRequestException('Movie Does not exists')


# user = User.objects.get(id=user.id)
# user.photo.save(image_path, image)
# user.save()
