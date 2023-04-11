'''
from sklearn.metrics.pairwise import cosine_similarity
from numpy import mean
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from .models import User, Movie, FavouriteMovie



def get_all_users_movies():
    all_users_movies = {}
    for user in User.objects.all():
        user_movies = {}
        for favourite_movie in user.favouritemovie_set.select_related('movie'):
            movie = favourite_movie.movie
            user_movies[movie.title] = movie
        all_users_movies[user.id] = user_movies
    return all_users_movies

# all_users_movies = get_all_users_movies()
# matches = match_users_cosine(c_user_id=1, all_users_movies=all_users_movies)


def match_users_cosine(c_user_id):
    all_users_movies = get_all_users_movies()
    current_user = User.objects.get(id=c_user_id)
    current_user_movies = all_users_movies[c_user_id]

    matches = []

    for user_id, user_movies in all_users_movies.items():
        if user_id == c_user_id or not user_movies:
            continue

        # calculate cosine similarity between user and current_user's favourite movies
        common_titles = set(current_user_movies.keys()).intersection(set(user_movies.keys()))
        if not common_titles:
            continue

        # filter movies by common titles
        current_user_filtered_movies = [current_user_movies[title] for title in common_titles]
        user_filtered_movies = [user_movies[title] for title in common_titles]

        # create feature vectors for each user's movie preferences
        current_user_features = [movie.get_features() for movie in current_user_filtered_movies]
        user_features = [movie.get_features() for movie in user_filtered_movies]

        # calculate cosine similarity between feature vectors
        # similarity = cosine_similarity(current_user_features, user_features)
        # create one-hot encoder
        encoder = OneHotEncoder()

        # get current user features
        current_user_features = []
        for movie in current_user_filtered_movies:
            current_user_features.append(movie.get_features())

        # encode current user features
        current_user_encoded = encoder.fit_transform(current_user_features).toarray()

        # get user features
        user_features = []
        for movie in user_filtered_movies:
            user_features.append(movie.get_features())

        # encode user features
        user_encoded = encoder.transform(user_features).toarray()

        # calculate cosine similarity between feature vectors
        similarity = cosine_similarity(current_user_encoded, user_encoded)
        similarity_score = mean(similarity)

        # assign weights to different aspects of the matching algorithm
        gender_weight = 0.3
        sexuality_weight = 0.3
        movie_weight = 0.4

        # calculate match score
        user = User.objects.get(id=user_id)
        match_score = (gender_weight * (current_user.profile.gender == user.profile.gender)) + \
                      (sexuality_weight * (current_user.profile.sexuality == user.profile.sexuality)) + \
                      (movie_weight * similarity_score)

        if match_score > 0.5:
            matches.append({'user': user, 'score': match_score})

    return matches
'''