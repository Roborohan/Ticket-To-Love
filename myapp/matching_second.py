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
        elif user_profile.gender == 'F':
            gender = 'M'
        else:
            gender = 'O'
        matched_profiles = Profile.objects.filter(
            Q(gender=gender, sexuality__in=['H', 'B']) |
            Q(gender=user_profile.gender, sexuality='N')
        ).exclude(user=user_profile.user)
    elif user_profile.sexuality == 'G':
        matched_profiles = Profile.objects.filter(
            Q(gender=user_profile.gender, sexuality__in=['G', 'B']) |
            Q(sexuality='N')
        ).exclude(user=user_profile.user)
    elif user_profile.sexuality == 'B':
        if user_profile.gender == 'M':
            gender = 'F'
            opp_gender = 'M'
        elif user_profile.gender == 'F':
            gender = 'M'
            opp_gender = 'F'
        else:
            gender = 'O'
            opp_gender = 'O'
        matched_profiles = Profile.objects.filter(
            Q(gender=gender, sexuality__in=['H', 'G', 'B']) |
            Q(gender=opp_gender, sexuality__in=['G', 'B']) |
            Q(sexuality='N')
        ).exclude(user=user_profile.user)
    elif user_profile.sexuality == 'N':
        matched_profiles = Profile.objects.filter(
            Q(sexuality__in=['H', 'G', 'B', 'N']) |
            Q(gender=user_profile.gender, sexuality='B') |
            Q(gender=user_profile.gender, sexuality=user_profile.sexuality)
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

        match_score = weighted_sum * size_factor
        print(f"Match score for user {user_id}: {match_score}")

        if match_score > 1.1:
            matches.append({'user': user, 'score': round(match_score, 2)})

    return matches
