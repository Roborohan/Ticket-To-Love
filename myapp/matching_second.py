from operator import delitem
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import hmean
from numpy import mean
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from .models import User, Movie, FavouriteMovie
from users.models import  Profile
from django.db.models import Q

def filter_users(user_id):
    matched_profiles = []
    user_profile = User.objects.get(pk=user_id).profile

    if user_profile.sexuality == 'H':
        if user_profile.gender == 'M':
            gender = 'F'
            matched_profiles = Profile.objects.filter(
                Q(gender=gender, sexuality='H') |
                Q(gender=gender, sexuality='B') |
                Q(gender=gender, sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gender == 'F':
            gender = 'M'
            matched_profiles = Profile.objects.filter(
                Q(gender=gender, sexuality='H') |
                Q(gender=gender, sexuality='B') |
                Q(gender=gender, sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gendr == 'O':
            gender = 'O'
            matched_profiles = Profile.objects.filter(
                Q(gender=gender, sexuality='H') |
                Q(gender=gender, sexuality='B') |
                Q(gender=gender, sexuality='G') |
                Q(gender=gender, sexuality='N')
            ).exclude(user=user_profile.user)

    elif user_profile.sexuality == 'G':
        if user_profile.gender == 'M':
            gender = 'M'
            matched_profiles = Profile.objects.filter(
                Q(gender=gender, sexuality='G') |
                Q(gender=gender, sexuality='B') |
                Q(gender=gender, sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gender == 'F':
            gender = 'F'
            matched_profiles = Profile.objects.filter(
                Q(gender=gender, sexuality='G') |
                Q(gender=gender, sexuality='B') |
                Q(gender=gender, sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gender == 'O':
            gender = 'O'
            matched_profiles = Profile.objects.filter(
                Q(gender=gender, sexuality='G') |
                Q(gender=gender, sexuality='B') |
                Q(gender=gender, sexuality='N') |
                Q(gender=gender, sexuality='H')
            ).exclude(user=user_profile.user)

    elif user_profile.sexuality == 'B':
        if user_profile.gender == 'M':
            matched_profiles = Profile.objects.filter(
                Q(gender='F', sexuality='H') |
                Q(gender='F', sexuality='B') |
                Q(gender='F', sexuality='N') |
                Q(gender='M', sexuality='B') |
                Q(gender='M', sexuality='G') |
                Q(gender='M', sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gender == 'F':
            matched_profiles = Profile.objects.filter(
                Q(gender='M', sexuality='H') |
                Q(gender='M', sexuality='B') |
                Q(gender='M', sexuality='N') |
                Q(gender='F', sexuality='B') |
                Q(gender='F', sexuality='G') |
                Q(gender='F', sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gender == 'O':
            gender = 'O'
            matched_profiles = Profile.objects.filter(
                Q(gender=gender, sexuality='G') |
                Q(gender=gender, sexuality='B') |
                Q(gender=gender, sexuality='N') |
                Q(gender=gender, sexuality='H')
            ).exclude(user=user_profile.user)

    elif user_profile.sexuality == 'N':
        if user_profile.gender == 'M':
            matched_profiles = Profile.objects.filter(
                Q(gender='F', sexuality='B') |
                Q(gender='F', sexuality='N') |
                Q(gender='M', sexuality='B') |
                Q(gender='M', sexuality='G') |
                Q(gender='M', sexuality='N') |
                Q(gender='O', sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gender == 'F':
            matched_profiles = Profile.objects.filter(
                Q(gender='F', sexuality='B') |
                Q(gender='F', sexuality='G') |
                Q(gender='F', sexuality='N') |
                Q(gender='M', sexuality='B') |
                Q(gender='M', sexuality='N') |
                Q(gender='O', sexuality='N')
            ).exclude(user=user_profile.user)
        elif user_profile.gender == 'O':
            matched_profiles = Profile.objects.filter(
                Q(gender='O', sexuality='H') |
                Q(gender='O', sexuality='G') |
                Q(gender='O', sexuality='B') |
                Q(gender='O', sexuality='N') |
                Q(gender='M', sexuality='N') |
                Q(gender='F', sexuality='N')
            ).exclude(user=user_profile.user)

    return matched_profiles






def get_all_users_movies(c_user_id):
    all_users_movies = {}
    for user in filter_users(c_user_id): #User.objects.all(pk=c_user_id):
        user = User.objects.get(id=user.id)
        user_movies = {}
        for favourite_movie in user.favouritemovie_set.select_related('movie'):
            movie = favourite_movie.movie
            user_movies[movie.id] = movie
        all_users_movies[user.id] = user_movies
    return all_users_movies

def get_current_user_movies(c_user_id):
    current_user_movies = {}
    user = User.objects.get(id=c_user_id)
    for favourite_movie in user.favouritemovie_set.select_related('movie'):
        movie = favourite_movie.movie
        current_user_movies[movie.id] = movie

    return current_user_movies



def match_users_cosine(c_user_id):
    all_users_movies = get_all_users_movies(c_user_id)
    current_user_movies = get_current_user_movies(c_user_id)

    current_user_features = []
    for movie in list(current_user_movies.values()):
        try:
            features = movie.get_features()
            current_user_features.extend(features)
        except AttributeError:
            print("Getting error")
            pass

    matches = []

    for user_id, user_movies in all_users_movies.items():
        if user_id == c_user_id or not user_movies:
            continue

        user_features = []

        for movie in list(user_movies.values()):
            try:
                features = movie.get_features()
                user_features.extend(features)
            except AttributeError:
                print(f"Warning: movie {movie.title} does not have a get_features() method.")

        all_features = current_user_features + user_features

        encoder = OneHotEncoder()
        # Fit the encoder on all_features
        encoder.fit(all_features)

        # Transform the features of both users using the same encoder
        current_user_encoded = encoder.transform(current_user_features).toarray()
        user_encoded = encoder.transform(user_features).toarray()

        # Calculate similarity scores for each feature
        similarity_scores = {}
        for feature in ['title', 'genre', 'director', 'actor']:
            feature_indices = [i for i, x in enumerate(encoder.categories_[0]) if x.startswith(feature)]
            similarity = cosine_similarity(current_user_encoded[:, feature_indices], user_encoded[:, feature_indices])
            similarity_scores[feature] = mean(similarity)

        movie_title_weight = 0.5
        movie_genre_weight = 0.2
        movie_actors_weight = 0.4
        movie_director_weight = 0.4

        user = User.objects.get(id=user_id)

        # Calculate the harmonic mean of the number of movies for both users
        size_factor = hmean([len(current_user_features), len(user_features)])

        print(f"Similarity scores for user {user_id}: {similarity_scores}")

        weighted_sum = (
            (movie_director_weight * similarity_scores['director']) +
            (movie_genre_weight * similarity_scores['genre']) +
            (movie_actors_weight * similarity_scores['actor']) +
            (movie_title_weight * similarity_scores['title'])
        )

        print(f"Weighted sum for user {user_id}: {weighted_sum}")

        match_score = weighted_sum * size_factor  #normalisation for accounts with different numbers of movies
        print(f"Match score for user {user_id}: {match_score}")

        if match_score > 2: #threshold to display user matches
            matches.append({'user': user, 'score': round(match_score, 2)})

    return matches
