from django.urls import path

from . import views

app_name = "movies"

urlpatterns = [
    path('add/', views.AddMovieApi.as_view(), name='add_movie'),
    path('add/comment/', views.AddMovieCommentApi.as_view(), name='add_movie_comment'),
    path('get/newest/', views.GetNewestMoviesApi.as_view(), name='get_new_movies'),
    path('detail/<int:movie_id>/', views.MovieDetailApi.as_view(), name='get_movie_detail'),
    path("favorite/add/<int:movie_id>/", views.AddFavoriteMovieApi.as_view(), name="add_favorite_movie"),
    path("favorite/remove/<int:movie_id>/", views.RemoveFavoriteMovieApi.as_view(), name="remove_favorite_movie"),
    path('favorite/all/', views.GetFavoriteMoviesApi.as_view(), name='get_favorite_movies'),
    path('search/<str:query>/', views.SearchMovieApi.as_view(), name='search_movie'),
    path('add-genres/', views.GetGenresApi.as_view(), name='get_all_genres_for_admin'),
    path('all/genre/<str:genre_slug>/', views.GetMoviesByGenreApi.as_view(), name='get_movie_by_genre'),
    path('genres/', views.GetPublicGenresApi.as_view(), name='get_all_genres'),
    path('favorite/exists/<int:movie_id>/', views.IsUserFavoriteApi.as_view(), name='check_user_favorite'),
]
