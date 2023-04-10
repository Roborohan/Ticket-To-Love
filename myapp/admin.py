from django.contrib import admin

# Register models here.
from .models import Movie,FavouriteMovie, Match
 

class MovieAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'genre', 'director','actors','release_date','country','year','created_at')
admin.site.register(Movie, MovieAdmin)

class FavouriteMovieAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'movie')
admin.site.register(FavouriteMovie, FavouriteMovieAdmin)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('id','user1', 'user2','confirmed_by_user1','confirmed_by_user2','is_blocked')
admin.site.register(Match, MatchAdmin)
