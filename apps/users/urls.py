from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


app_name = "users"
urlpatterns = [
    path("register/email/", views.EmailRegistrationApi.as_view(), name="validate_email_register"),
    path("register/", views.RegisterUserApi.as_view(), name="user_register"),
    path("upload/profile-image/", views.UploadProfileImageApi.as_view(), name="upload_profile_image"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/me/", views.UserSelfProfileApi.as_view(), name="logged_in_user_profile"),
    path("profile/<str:username>/", views.UserProfileApi.as_view(), name="user_profile"),
    path("update/profile/", views.UpdateUserInfoApi.as_view(), name="update_user_profile"),
    path("follow/<str:username>/", views.UserFollowApi.as_view(), name="user_follow"),
    path("unfollow/<str:username>/", views.UserUnfollowApi.as_view(), name="user_follow"),
    path("search/<str:query>/", views.SearchUserApi.as_view(), name="search_users"),
    path("followings/me/", views.GetSelfFollowingListApi.as_view(), name="get_followings_current_user"),
    path("followers/me/", views.GetSelfFollowersListApi.as_view(), name="get_followers_current_user"),
    path("followings/<str:username>/", views.GetFollowingListApi.as_view(), name="get_followings"),
    path("followers/<str:username>/", views.GetFollowersListApi.as_view(), name="get_followers"),
    path('follow-exists/<str:username>/', views.IsUserFriendApi.as_view(), name='is_user_friend'),
    path('recommend/movie/', views.RecommendMovieToUserApi.as_view(), name='recommend_movie_to_user'),
    path('recommend/answer/', views.AnswerRecommendedMovieApi.as_view(), name='answer_recommended_movie'),
    path('recommend/get/all/', views.GetRecommendedMoviesApi.as_view(), name='get_my_recommended_movies'),
    path('recommend/get/answers/all/', views.GetRecommendedMovieAnswersApi.as_view(),
         name='get_my_recommended_answers'),
    path('recommend/remove/<int:recommend_id>/', views.RemoveRecommendedMovieApi.as_view(),
         name='remove_recommended_movie'),
    path('recommend/answer/remove/<int:answer_id>/', views.RemoveRecommendAnswerApi.as_view(), name='remove_answer'),
]
