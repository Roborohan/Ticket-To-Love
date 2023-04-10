import datetime
from django.db import IntegrityError

from django.views import View
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, FavouriteMovie
# from myapp.matching_algorithm import *
from myapp.matching_second import *

from django.contrib.auth.models import User
# Create views here.
def home(request):
    return render(request, 'users/home.html')

# https://www.omdbapi.com/?apikey=REDACTED_API_KEY&t=titanic&y=1997

@login_required
def search_movies(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        year = request.POST.get('year')
        if query is None:
            return render(request, 'search_movies.html')
        if year:
            url = f'https://www.omdbapi.com/?apikey=REDACTED_API_KEY&s={query}&y={year}'
        else:
            url = f'https://www.omdbapi.com/?apikey=REDACTED_API_KEY&s={query}'
        response = requests.get(url)
        data = response.json()
        
        
        # Check if any movies were found
        if data['Response'] == 'True':
            search_results = data['Search']
            #iterate for each result to find the details 
            movies=[]
            for s_item in search_results:
                if s_item['imdbID']:
                    item_id=s_item['imdbID']
                    url_item = f'https://www.omdbapi.com/?apikey=REDACTED_API_KEY&i={item_id}'
                    item_details_response = requests.get(url_item)
                    
                    item_data = item_details_response.json()
                    
                    if item_data:
                        movies.append(item_data) 
            
            # Add 'is_favourite' flag to each movie in the search results
            user_favourites = FavouriteMovie.objects.filter(user=request.user)
             
            for movie in search_results:
                
                if user_favourites.filter(movie=movie['imdbID']).exists():
                    movie['is_favourite'] = True
                    
                else:
                    movie['is_favourite'] = False
                   
                movies.append(movie)               

            context = {'search_results': movies,'movie_ids':user_favourites}    
            return render(request, 'search_movies.html', context)
        
        else:
            error_message = data['Error']
            messages.add_message(request, messages.INFO, error_message)
            return render(request, 'search_movies.html')
    else:
        return render(request, 'search_movies.html')
 

@login_required
def favourite_movies(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie_title= request.POST.get('movie_title')
        genre= request.POST.get('genre')
        director= request.POST.get('director')
        actors= request.POST.get('actors')
        release_date= request.POST.get('release_date')
        country= request.POST.get('country')
        poster= request.POST.get('poster')
        year= request.POST.get('year')  
        #input validation 
        if not year or year.lower() in ['null', 'n/a', 'na', '']:
            year=2023
    
        # If release_date is null, N/A, NA, or empty, set a default date using the year passed by the user
        if not release_date or release_date.lower() in ['null', 'n/a', 'na', '']:           
            # Replace month and day to the beginning of the year
            release_date = datetime.datetime.strptime('', '%Y').date().replace(month=1, day=1,year=year)
         
        action = request.POST.get('action')
         
        if action == 'add':
            if not Movie.objects.filter(id=movie_id).exists():
                # If the movie ID does not exist in the Movies table, save the movie details        
                movie = Movie(id=movie_id, title=movie_title, genre=genre,director=director,actors=actors,release_date=release_date,country=country,poster=poster,year=year)
                # Create a new Movies object with the movie details
                try:
                    movie.save()
                    # Save the object to the database
                    messages.add_message(request, messages.INFO, 'Movie New Added.')
                except Exception as error_message:
                    messages.add_message(request, messages.INFO, error_message)


            else:
                movie= get_object_or_404(Movie, id=movie_id)
            if request.user.favouritemovie_set.count() >= 10:
                messages.add_message(request, messages.INFO, 'Limit Access , 10 Movies ')
                return redirect('myapp:home')
            try:
                FavouriteMovie.objects.create(user=request.user, movie=movie)
                messages.add_message(request, messages.INFO, 'Favourite Added')
            except IntegrityError:
                messages.add_message(request, messages.INFO, 'That movie is already in your favourites!')
            except Exception as error_message:
                    messages.add_message(request, messages.INFO, error_message)

            return redirect('myapp:home')
        else:
            movie = get_object_or_404(Movie, id=movie_id)
            FavouriteMovie.objects.filter(user=request.user, movie=movie).delete()
            messages.add_message(request, messages.INFO, 'Removed from Favourite list')
            return redirect('myapp:home')
    else:
        favourite_movies = request.user.favouritemovie_set.all()
        context = {'movies': favourite_movies}
        return render(request, 'favourite_movies.html', context)
@login_required
def remove_favourite(request):
    if request.method == 'POST':
        fav_movie_id = request.POST.get('fav_movie_id')         
        favourite_movie = FavouriteMovie.objects.filter(pk=fav_movie_id)
        favourite_movie.delete()
        messages.add_message(request, messages.INFO, 'Removed Success')
        return redirect('myapp:show_fav_movie')

@login_required
def un_favourite(request,movie_id):
    movie_id = request.POST.get('movie_id')
    movie= get_object_or_404(Movie, id=movie_id)
    FavouriteMovie.objects.filter(user=request.user, movie=movie).delete()
    messages.add_message(request, messages.INFO, 'Removed from Favourite list')
    return redirect('myapp:show_fav_movie')


@login_required
def add_favourite(request,movie_id):
    movie_id = request.POST.get('movie_id')
    movie= get_object_or_404(Movie, id=movie_id)
    FavouriteMovie.objects.create(user=request.user, movie=movie)
    messages.add_message(request, messages.INFO, 'In Favourite Added')
    return redirect('myapp:show_fav_movie')
 
@login_required
def make_favourite(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie= get_object_or_404(Movie, id=movie_id)
        user = get_object_or_404(User, id=request.user.id)      
        favourite_movie = FavouriteMovie.objects.create(user=user, movie=movie)
        messages.add_message(request, messages.INFO, 'In Favourite Added')
    return redirect('myapp:movie_list')
 
@login_required
def favourite_movies_show(request):
    favourite_movies = FavouriteMovie.objects.filter(user=request.user)
    context = {'favourite_movies': favourite_movies, 'count': favourite_movies.count()}
    return render(request, 'favourite_movies.html', context)

@login_required
def friend_favourite_movies(request,friend_id):
    favourite_movies = FavouriteMovie.objects.filter(user=friend_id)
    context = {'favourite_movies': favourite_movies, 'count': favourite_movies.count()}
    return render(request, 'friend_favourite_movies.html', context)

@login_required
def match(request):
    # algo_match=match_users_cosine(request.user.id)
    try:
        algo_matches = match_users_cosine(request.user.id)
        # Order matches by score in descending order
        algo_matches = sorted(algo_matches, key=lambda x: x['score'], reverse=True)
    except IndexError:
        algo_matches = None
    print(algo_matches)
    context={'algo_matches':algo_matches,'count':2}
    return render(request, 'match.html', context)

@login_required
def movie_list(request):
    movie_list = Movie.objects.all()
    user_favourites = FavouriteMovie.objects.filter(user=request.user)
    movies = []
    for movie in movie_list:
        if user_favourites.filter(movie=movie.id).exists():
            movie.is_favourite = True
        else:
            movie.is_favourite = False
        movies.append(movie)

  
    context = {'movie_list': movies,'count':movie_list.count()}
    return render(request, 'movie_list.html', context)