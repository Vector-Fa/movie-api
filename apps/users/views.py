from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import (UserRegisterSerializer, UserSerializer, SearchUserOutputSerializer,
                          EmailRegisterationSerializer, UserFriendListSerializer, UploadProfileImageSerializer,
                          UpdateUserSerializer, RecommendMovieToUserSerializer, AnswerRecommendedMovieSerializer,
                          AnswerRecommendedMovieOutSerializer, GetRecommendedMoviesOutSerializer)
from .models import User, MovieRecommend, MovieRecommendAnswer
from .services import (UserFollowService, check_registration_email, UploadProfileImageService,
                       register_user, search_user, is_user_friend, FollowListService,
                       MovieRecommendService)
from ..custom_response import SuccessResponse
from ..utils import is_serializer_valid, get_or_404


class EmailRegistrationApi(APIView):
    """
    validate if registration email already exists or not, and send verify code
     -> Success message
    """
    serializer_class = EmailRegisterationSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        is_serializer_valid(ser_data)
        return check_registration_email(email=ser_data.validated_data['email'])


class RegisterUserApi(APIView):
    """
    Register user & validate verify code
     -> New[User]
    """
    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        is_serializer_valid(ser_data)

        data = ser_data.validated_data
        user = register_user(
            username=data['username'], email=data['email'],
            password=data['password'], verify_code=data['verify_code']
        )
        new_data = self.serializer_class(instance=user)
        return SuccessResponse({'user': new_data.data}, status=status.HTTP_201_CREATED)


class UploadProfileImageApi(APIView):
    """
    endpoint for users to upload their profile image
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UploadProfileImageSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        is_serializer_valid(ser_data)
        return UploadProfileImageService().upload(ser_data.validated_data['image'], user=request.user)


class UpdateUserInfoApi(APIView):
    """
    user can update its personal info
     -> Updated[User]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def patch(self, request):
        ser_data = self.serializer_class(instance=request.user, data=request.data, partial=True)
        is_serializer_valid(ser_data)
        ser_data.save()
        return SuccessResponse({'user': ser_data.data})


class UserSelfProfileApi(APIView):
    """
    Endpoint for logged-in user to see his profile
     -> User
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        ser_data = self.serializer_class(instance=request.user)
        return Response({'user': ser_data.data}, status=200)


class UserProfileApi(APIView):
    """
    User can see its profile
     -> User
    """
    serializer_class = UserSerializer

    def get(self, request, username: str):
        user = get_or_404(User, username=username)
        ser_data = self.serializer_class(instance=user)
        return SuccessResponse({'user': ser_data.data})


class UserFollowApi(APIView):
    """
    Endpoint to let user follow another person
     -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request, username: str):
        return UserFollowService(user=request.user, to_username=username).follow()


class UserUnfollowApi(APIView):
    """
    Endpoint to let user unfollow their friends
     -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def delete(self, request, username: str):
        return UserFollowService(user=request.user, to_username=username).unfollow()


class SearchUserApi(APIView):
    """
    Search in users
     -> List[User]
    """
    serializer_class = SearchUserOutputSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, query: str):
        users = search_user(query)
        ser_data = SearchUserOutputSerializer(instance=users, many=True)
        return SuccessResponse({'users': ser_data.data})


class GetFollowingListApi(APIView):
    """
    get all the user which this username follows
     -> List[User]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserFriendListSerializer

    def get(self, request, username: str):
        user_from = get_or_404(User, username=username)
        followings = FollowListService.get_followings(user_from)
        ser_data = UserFriendListSerializer(instance=followings, many=True)
        return SuccessResponse({'users': ser_data.data})


class GetFollowersListApi(APIView):
    """
    get all the users that follows this username
     -> List[User]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserFriendListSerializer

    def get(self, request, username: str):
        user_to = get_or_404(User, username=username)
        followers = FollowListService.get_followers(user_to)
        ser_data = UserFriendListSerializer(instance=followers, many=True)
        return SuccessResponse({'users': ser_data.data})


class GetSelfFollowingListApi(APIView):
    """
    get all the user which logged-in user follows
     -> List[User]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserFriendListSerializer

    def get(self, request):
        followings = FollowListService.get_followings(request.user)
        ser_data = UserFriendListSerializer(instance=followings, many=True)
        return SuccessResponse({'users': ser_data.data})


class GetSelfFollowersListApi(APIView):
    """
    get all the users that follows logged in user
     -> List[User]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserFriendListSerializer

    def get(self, request):
        followers = FollowListService.get_followers(request.user)
        ser_data = UserFriendListSerializer(instance=followers, many=True)
        return SuccessResponse({'users': ser_data.data})


class IsUserFriendApi(APIView):
    """
    Is this username in current user follower list
    -> True/False message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def get(self, request, username: str):
        return is_user_friend(username, request.user)


class RecommendMovieToUserApi(APIView):
    """
    Users can recommend movies to their followings
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = RecommendMovieToUserSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        is_serializer_valid(ser_data)
        data = ser_data.validated_data
        return MovieRecommendService(user_from=request.user).recommend_to_user(username_to=data['username'],
                                                                               movie_id=data['movie_id'])


class AnswerRecommendedMovieApi(APIView):
    """
    User can answer back if they (liked it, already watched or didn't like it) to user where recommended that movie
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerRecommendedMovieSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        is_serializer_valid(ser_data)
        data = ser_data.validated_data
        return MovieRecommendService(user_from=request.user).answer_recommended_movie(
            answer_status=data['answer_status'], recommend_id=data['recommend_id'])


class GetRecommendedMoviesApi(APIView):
    """
    Get a list of movies that other users recommended to logged-in user
    -> List[Movie]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GetRecommendedMoviesOutSerializer

    def get(self, request):
        recommends = request.user.recommended_movies.select_related('movie').all()
        ser_data = self.serializer_class(instance=recommends, many=True)
        return SuccessResponse({'recommended_movies': ser_data.data})


class GetRecommendedMovieAnswersApi(APIView):
    """
    Get a list of answers where logged-in user sent recommended movies to them
    -> List[MovieRecommendAnswer]
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerRecommendedMovieOutSerializer

    def get(self, request):
        recommended_answers = request.user.answer_got_recommended.all()
        ser_data = self.serializer_class(instance=recommended_answers, many=True)
        return SuccessResponse({'answers': ser_data.data})


class RemoveRecommendedMovieApi(APIView):
    """
    User can delete its recommendation without answering it
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def delete(self, request, recommend_id: int):
        recommended_movie = get_or_404(MovieRecommend, pk=recommend_id)
        recommended_movie.delete()
        return SuccessResponse({'message': 'deleted successfully'})


class RemoveRecommendAnswerApi(APIView):
    """
    User can remove its answer where sent by other users
    -> Success message
    """
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def delete(self, request, answer_id: int):
        answer_instance = get_or_404(MovieRecommendAnswer, pk=answer_id)
        answer_instance.delete()
        return SuccessResponse({'message': 'deleted successfully'})


