from django.urls import path
 
from . import views
# from .views import search_movies,remove_favourite, favourite_movies,match,movie_list,favourite_movies_show
 
app_name = 'myapp'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('search/', views.search_movies, name='search'),
    path('show_fav_movie/', views.favourite_movies_show, name='show_fav_movie'),
    path('show_fav_movie/<int:friend_id>/', views.friend_favourite_movies, name='friend_favourite_movies'),
    path('remove_favourite/', views.remove_favourite, name='remove_favourite'),
    path('un_favourite/<str:movie_id>/', views.un_favourite, name='un_favourite'),
    path('favourites/', views.favourite_movies, name='favourite_movies'),
    path('add_favourite/<str:movie_id>/', views.add_favourite, name='add_favourite'),
    path('match/', views.match, name='match'),
    path('movie_list/', views.movie_list, name='movie_list'), 
    path('make_favourite/', views.make_favourite, name='make_favourite'), 
      
]
