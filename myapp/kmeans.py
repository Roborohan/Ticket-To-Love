from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Profile, Movie
from .forms import ProfileForm
from sklearn.cluster import KMeans


def match_users(request):
    # Get all the profiles
    profiles = Profile.objects.all()

    # Create a matrix with users and their favourite movies
    data = []
    for profile in profiles:
        row = []
        row.append(profile.id)
        row.append(profile.gender)
        row.append(profile.sexuality)
        movies = Movie.objects.filter(profile=profile)
        for movie in movies:
            row.append(movie.title)
            row.append(movie.actors)
            row.append(movie.director)
            row.append(movie.genre)
            row.append(movie.release_year)
        data.append(row)

    # Define weights for each movie attribute
    weights = [3, 1, 1, 2, 1]

    # Cluster the users based on their favourite movies
    kmeans = KMeans(n_clusters=2, random_state=0).fit(data)

    # Get the cluster assignments for each user
    cluster_assignments = kmeans.labels_

    # Create a dictionary to store the matches
    matches = {}

    # Iterate over the users and their cluster assignments
    for profile, cluster_assignment in zip(profiles, cluster_assignments):
        # If the user is not already in the matches dictionary, add them
        if profile not in matches:
            matches[profile] = []
        # Add the user to their assigned cluster
        matches[profile].append(cluster_assignment)

    # Return the matches as a JSON response
    return JsonResponse(matches)


@login_required
def matches(request):
    # Get the current user's profile
    profile = request.user.profile

    # Get all the profiles except the current user's
    profiles = Profile.objects.exclude(user=request.user)

    # Call the match_users function to get the matches
    matches = match_users(request)

    # Render the matches page with the matches and the current user's profile
    return render(request, 'matches.html', {'matches': matches, 'profile': profile, 'profiles': profiles})
    
    
    
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from django.db.models import Q

# Function to calculate the similarity score between two sets of favourite films
def calculate_similarity_score(favourites1, favourites2):
    set1 = set(favourites1.split(','))
    set2 = set(favourites2.split(','))
    common_favourites = set1 & set2
    return len(common_favourites)

@login_required
def matches(request):
    current_user = request.user
    # Get all users except the current user
    users = User.objects.exclude(username=current_user.username).filter(is_active=True)

    # Filter users by sexuality and gender
    filtered_users = users.filter(Q(sexuality=current_user.gender) | Q(sexuality='Both'),
                                  gender=current_user.sexuality)

    # Create a list of favourite films for all users
    favourite_films = [user.profile.favourites for user in filtered_users]

    # Cluster the favourite films using KMeans
    num_clusters = min(len(favourite_films), 5)
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(favourite_films)

    # Assign each user to a cluster
    clusters = [[] for i in range(num_clusters)]
    for i, label in enumerate(kmeans.labels_):
        clusters[label].append(filtered_users[i])

    # Get the closest match in each cluster
    matches = []
    for cluster in clusters:
        if len(cluster) > 1:
            for user in cluster:
                # Find the closest user in the same cluster
                idx = pairwise_distances_argmin_min(kmeans.cluster_centers_, [user.profile.favourites])[0][0]
                closest_user = cluster[idx]
                if closest_user != user:
                    # Calculate the similarity score between the two users' favourite films
                    score = calculate_similarity_score(user.profile.favourites, closest_user.profile.favourites)
                    matches.append({'user1': user, 'user2': closest_user, 'score': score})

    # Sort the matches by score in descending order
    matches = sorted(matches, key=lambda x: x['score'], reverse=True)

    return render(request, 'matches.html', {'matches': matches})


