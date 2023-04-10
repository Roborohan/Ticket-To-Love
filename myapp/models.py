from django.db import models
from datetime import datetime

from django.contrib.auth.models import User
# Create models here.
class Movie(models.Model):
    id  =models.CharField(max_length=20, primary_key = True)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    actors = models.CharField(max_length=200)
    release_date = models.CharField(max_length=20)
    country = models.CharField(max_length=50)
    poster = models.URLField()
    year = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    def get_features(self):
        features = [
            ('title', self.title),
        ]
            
        genres = [('genre', genre.strip()) for genre in self.genre.split(',')]
        features.extend(genres)
            
        directors = [('director', director.strip()) for director in self.director.split(',')]
        features.extend(directors)
            
        actors = [('actor', actor.strip()) for actor in self.actors.split(',')]
        features.extend(actors)
            
        return features




    class Meta:
        ordering = ['-created_at']  

class FavouriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'movie'),)     
    def __str__(self):
        return self.movie.id
    def __int__(self):
        return self.id


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1_matches')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2_matches')
    confirmed_by_user1 = models.BooleanField(default=False)
    confirmed_by_user2 = models.BooleanField(default=False)
    is_blocked  = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user1', 'user2')
